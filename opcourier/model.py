from docplex.mp.model import Model
from docplex.util.environment import get_environment
import marshmallow_dataclass

from pyknapsack.data import KnapsackData, KnapsackResult


def execute(input_file: str = "data/data.json", output_file: str = "data/solution.json"):
    import json
    import docplex.util.environment as environment

    data_schema = marshmallow_dataclass.class_schema(KnapsackData)()
    result_schema = marshmallow_dataclass.class_schema(KnapsackResult)()

    # open program input named "data.txt" and sum the contents
    with environment.get_input_stream(input_file) as input:
        data = data_schema.load(json.load(input))

        result = solve(data)

        # write the result as a simple json in program output "solution.json"
        with environment.get_output_stream(output_file) as output:
            output.write(json.dumps(result_schema.dump(result)).encode('utf-8'))


def simulate():
    # import json
    # import docplex.util.environment as environment
    data: KnapsackData = KnapsackData(items=[(1, 10, 20), (2, 5, 28), (3, 2, 17), (4, 5, 38), (5, 4, 38)], capacity=10)
    # with environment.get_output_stream("data.json") as output:
    #    data_schema = marshmallow_dataclass.class_schema(KnapsackData)()
    #    data_dict = data_schema.dump(data)
    #    output.write(json.dumps(data_dict).encode('utf-8'))
    result = solve(data)
    print(result)


def solve(data: KnapsackData):

    model = Model(name='knapsack')
    model.ids, model.pesos, model.valores = zip(*data.items)
    model.capacidad = data.capacity

    model.objeto_escogido = model.binary_var_list(model.ids)
    model.add_constraint(model.capacidad >= model.sum(model.objeto_escogido[n] * model.pesos[n] for n in range(len(model.pesos))))
    model.maximize(model.sum(model.objeto_escogido[n] * model.valores[n] for n in range(len(model.valores))))

    model.parameters.threads = 2
    model.parameters.timelimit = 120  # nurse should not take more than that !
    sol = model.solve(log_output=True)

    if sol is not None:
        selected_items = []  
        for var in model.objeto_escogido:
            if (sol[var] > 0.5): selected_items = selected_items + [var.name]
        result = KnapsackResult(items=selected_items, usedCapacity=0, profit=model.objective_value, solved=True, time=0)
        print("solution for a cost of {}".format(model.objective_value))
        print(' '.join(str(p) for p in selected_items))
        return result
    else:
        print("* model is infeasible")


#execute()
simulate()