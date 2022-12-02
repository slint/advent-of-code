TOP_COUNT = 3

def run(input_data: str):

    top_snacks = [0] * TOP_COUNT

    snack_calories = [
        sum(int(i) for i in snack_list.split())
        for snack_list in input_data.split('\n\n')
    ]

    for cur_snack in snack_calories:
        for idx in range(TOP_COUNT):
            if cur_snack >= top_snacks[idx]:
                cur_snack, top_snacks[idx] = top_snacks[idx], cur_snack

    print(f"Part one: {max(top_snacks)}")
    print(f"Part two: {sum(top_snacks)}")
