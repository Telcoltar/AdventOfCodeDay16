import logging
from argparse import ArgumentParser, Namespace
from typing import TextIO

from Field import Field

parser: ArgumentParser = ArgumentParser()

parser.add_argument("--log", default="info")

options: Namespace = parser.parse_args()

level = logging.DEBUG

if options.log.lower() == "info":
    level = logging.INFO

logging.basicConfig(format='%(asctime)s | %(name)s | %(levelname)s | %(message)s',
                    level=level)

logger: logging.Logger = logging.getLogger(__name__)


def get_input_data(file_name: str) ->tuple[list[Field], list[int], list[list[int]]]:
    f: TextIO = open(file_name)
    current_line: str = f.readline().strip()
    field_identifer: str
    ranges: str
    lower_range: str
    higher_range: str
    field_list: list[Field] = []
    my_ticket: list[int]
    nearby_ticket_list: list[list[int]] = []
    while current_line != "":
        logger.debug(current_line)
        field_identifer, ranges = current_line.split(":")
        lower_range, higher_range = ranges.split("or")
        field_list.append(Field(field_identifer.strip(), lower_range.strip(), higher_range.strip()))
        current_line = f.readline().strip()
    logger.debug(f.readline().strip())
    my_ticket = list(map(int, f.readline().strip().split(",")))
    f.readline()
    logger.debug(f.readline().strip())
    current_line = f.readline().strip()
    while current_line != "":
        logger.debug(current_line)
        nearby_ticket_list.append(list(map(int, current_line.split(","))))
        current_line = f.readline().strip()
    return field_list, my_ticket, nearby_ticket_list


def test_value_agains_all_fields(value: int, field_list: list[Field]) -> bool:
    for field in field_list:
        if field.is_number_valid(value):
            return True
    return False


def is_ticket_valid(ticket: list[int], field_list: list[Field]) -> bool:
    for val in ticket:
        if not test_value_agains_all_fields(val, field_list):
            return False
    return True


def is_field_valid_for_val_list(vals: list[int], field: Field) -> bool:
    for val in vals:
        if not field.is_number_valid(val):
            return False
    return True


def solution_part_1(file_name: str) -> int:
    field_list, _, nearby_ticket_list = get_input_data(file_name)
    error_rate: int = 0
    for ticket in nearby_ticket_list:
        for val in ticket:
            if not test_value_agains_all_fields(val, field_list):
                error_rate += val
    return error_rate


def transpose_ticket_list(ticket_list: list[list[int]]) -> list[list[int]]:
    resulting_list: list[list[int]] = []
    val_list: list[int]
    for i in range(len(ticket_list[0])):
        val_list = []
        for ticket in ticket_list:
            val_list.append(ticket[i])
        resulting_list.append(val_list)
    return resulting_list


def is_field_in_dense_fields(field: Field, dense_fields: list[tuple[int, Field]]):
    for dense_field in dense_fields:
        if field.identifier == dense_field[1].identifier:
            return True
    return False


def solution_part_2(file_name: str) -> int:
    field_list, my_ticket, nearby_ticket_list = get_input_data(file_name)
    valid_ticket_list: list[list[int]] = []
    for ticket in nearby_ticket_list:
        if is_ticket_valid(ticket, field_list):
            valid_ticket_list.append(ticket)
    resulting_fields: list[tuple[int, list[Field]]] = []
    current_field_list: list[Field]
    transpose_valid_ticket_list = transpose_ticket_list(valid_ticket_list)
    for i, vals in enumerate(transpose_valid_ticket_list):
        current_field_list = []
        for field in field_list:
            if is_field_valid_for_val_list(vals, field):
                current_field_list.append(field)
        resulting_fields.append((i, current_field_list))
    field_val: int = 1
    resulting_fields.sort(key=lambda res_field_list: len(res_field_list[1]))
    dense_result_fields: list[tuple[int, Field]] = []
    index: int
    for field_index, fields in resulting_fields:
        for field in fields:
            if not is_field_in_dense_fields(field, dense_result_fields):
                dense_result_fields.append((field_index, field))
                break
    logger.debug(dense_result_fields)
    for i, field in dense_result_fields:
        logger.debug(field.identifier)
        if "departure" in field.identifier:
            field_val *= my_ticket[i]
    return field_val


if __name__ == '__main__':
    logger.info(solution_part_1("inputData.txt"))
    logger.info(solution_part_2("inputData.txt"))
