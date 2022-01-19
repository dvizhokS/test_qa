#!/usr/bin/python3.8

def get_data(handler):
    file = open('app_2.log')
    lines = file.readlines()
    file.close()
    need_lines = []

    for line in lines:
        if handler in line:
            need_lines.append(line)

    return need_lines


def get_state_sensors(data_lines, sep=';'):
    data = {}

    for line in data_lines:
        l_index = line.find("'")
        r_index = line.rfind("'")
        clear_line = line[l_index:r_index].strip()
        arr = clear_line.split(sep)
        sens_id = arr[2]
        status = arr[-2]
        if sens_id in data:
            if status in data[sens_id]['state']:
                data[sens_id]['state'][status] += 1
            else:
                data[sens_id]['state'][status] = 1
        else:
            data[sens_id] = {'id': sens_id, 'state': {}}

    return data


def get_checking_data(sensors, success_state, error_state):
    removed = {}
    statuses = {}
    for sens_id in sensors:
        if error_state in sensors[sens_id]['state']:
            removed[sens_id] = 'removed'
        elif success_state in sensors[sens_id]['state']:
            statuses[sens_id] = sensors[sens_id]['state'][success_state]

    return removed, statuses


def get_check_sensors():
    data_lines = get_data('BIG')
    data_sensors = get_state_sensors(data_lines)
    sens_remove, sens_ok = get_checking_data(data_sensors, '02', 'DD')
    return sens_remove, sens_ok


def print_check_sensors(removed, success):
    header_text_removed = "______________Failed test {} devices_____________".format(len(removed))
    header_text_success = "______________Success test {} devices_____________".format(len(success))

    print(header_text_removed)
    for sens_id in removed:
        print("Devices {} was removed".format(sens_id))

    print(header_text_success)
    for sens_id in success:
        print("Devices {} sent {} statuses".format(sens_id, success[sens_id]))


def print_check_log():
    r, s = get_check_sensors()
    print_check_sensors(r, s)


if __name__ == "__main__":
    print_check_log()
