from dataclasses import dataclass
import csv
import os.path
# constants
SCRIPT_NAME = 'tip-assist'
SAVEFILE_HEADER = ['last_name', 'first_name', 'hours']
SAVEFILE_NAME = 'session.csv'
# commands and keywords
EXIT_COMMANDS = set(['quit', 'exit'])
INFO_COMMANDS = set(['info', 'help'])
LIST_COMMANDS = set(['list', 'ls'])
ADD_COMMANDS = set(['add'])
SET_COMMANDS = set(['set'])
UPDATE_COMMANDS = set(['update'])
REMOVE_COMMANDS = set(['remove', 'rem', 'rm'])
EMPLOYEE_KEYWORDS = set(['employee', 'employees'])
HOUR_KEYWORDS = set(['hour', 'hr', 'hours', 'hrs'])
DONE_KEYWORDS = set(['done', ''])

#region data classes
@dataclass
class employee_t:
    last_name: str
    first_name: str
    tippable_hrs: float = 0.0
    tip_rate: float = 0.0

@dataclass
class cash_denomination:
    name: str
    value: int
    def __hash__(self):
        return hash((self.name, self.value))

penny = cash_denomination("penny(ies)", 1)
nickel = cash_denomination("nickel(s)", 5)
dime = cash_denomination("dime(s)", 10)
quarter = cash_denomination("quarter(s)", 25)
half_dollar = cash_denomination("half dollar(s)", 50)
one_dollar = cash_denomination("one(s)", 1_00)
two_dollar = cash_denomination("two(s)", 2_00)
five_dollar = cash_denomination("five(s)", 5_00)
ten_dollar = cash_denomination("ten(s)", 10_00)
twenty_dollar = cash_denomination("twenty(ies)", 20_00)

default_stack = {
    penny: 0,
    nickel: 0,
    dime: 0,
    quarter: 0,
    one_dollar: 0,
    five_dollar: 0,
    ten_dollar: 0,
    twenty_dollar: 0
}
#endregion

# global state
employee_list = []
total_hours = 0.0
tips = []

def sort_employees():
    employee_list.sort(key=lambda e: f'{e.last_name}, {e.first_name}')

def calc_tip_rate():
    global total_hours
    total_hours = 0.0
    for e in employee_list:
        total_hours += e.tippable_hrs
    for e in employee_list:
        e.tip_rate = 0.0 if total_hours == 0 else e.tippable_hrs/total_hours


#region employee list management
def display_employees():
    print(f'{"":2}  {'Last Name':<13} {"First Name":<13} {"Tip Rate":<8}')
    for i, employee in enumerate(employee_list):
        print(f'{i + 1:>2}. {employee.last_name[:12] + ",":<13} {employee.first_name[:12]:<13} {employee.tip_rate:<3.3f}')

def add_employees():
    global employee_list
    print('Existing employees: ')
    display_employees()
    print('Enter new employee name in the format of "last,first"')
    print('or enter "done" to finish')
    done = False
    # loop to add employees
    while not done:
        raw_name_str = input('> ')
        tokenized_name = raw_name_str.strip().split(',')
        if tokenized_name[0] in DONE_KEYWORDS:
            done = True
        elif len(tokenized_name) != 2:
            print('unrecognized name format')
        else:
            employee_list.append(employee_t(
                last_name= tokenized_name[0].strip().upper(),
                first_name=tokenized_name[1].strip().upper()
            ))
    # sort employees via last name
    sort_employees()

def remove_employees():
    global employee_list
    done = False
    while not done:
        print('Employee list: ')
        display_employees()
        print('Enter the employee index to remove')
        print('or "done" to finish')
        is_invalid_command = False
        invalid_reason = ''
        raw_str = input('> ')
        tokenized_input = raw_str.strip().split()
        if tokenized_input[0] == 'done' or len(tokenized_input) == 0: #exit
            done = True
        # get index to remove
        elif tokenized_input[0].isdigit():
            employee_index = int(tokenized_input[0]) - 1
            # check boundary
            if employee_index >= 0 and employee_index < len(employee_list):
                employee_list.pop(employee_index)
            else:
                is_invalid_command = True
                invalid_reason = 'index out of bound'
        else:
            is_invalid_command = True
            invalid_reason = f'{tokenized_input[0]} is not a digit'
        if is_invalid_command:
            print('ERROR: ' + invalid_reason)
            print()
#endregion

def set_tippable_hrs():
    global employee_list
    # set tippable hrs
    for employee in employee_list:
        print(f'Current tippable hours for {employee.last_name}, {employee.first_name} is: {employee.tippable_hrs}')
        while True: # attempt to set hrs
            print(f'Set new hours for {employee.first_name}')
            raw_input = input('New hours (hit enter to keep current): ').strip()
            if raw_input == "":
                break
            try:
                hours = float(raw_input)
                employee.tippable_hrs = hours
                break #on success
            except ValueError:
                print(f'Unrecognized number {raw_input}')
    # set tip percent
    calc_tip_rate()

#region file IO
def load_session_from_file(filename):
    global employee_list
    employee_list = []
    with open(filename, 'r') as csvfile:
        savefile_reader = csv.DictReader(csvfile, SAVEFILE_HEADER)
        for employee in savefile_reader:
            print(f'adding {employee['first_name']}')
            new_employee = employee_t(
                last_name=employee['last_name'],
                first_name=employee['first_name'],
                tippable_hrs=float(employee['hours'])
            )
            employee_list.append(new_employee)
    sort_employees()
    calc_tip_rate()

def save_session_to_file(filename):
    with open(filename, 'w') as csvfile:
        savefile_writer = csv.DictWriter(csvfile, SAVEFILE_HEADER)
        for employee in employee_list:
            new_entry = {
                'last_name': employee.last_name,
                'first_name': employee.first_name,
                'hours': employee.tippable_hrs
            }
            savefile_writer.writerow(new_entry)
#endregion file IO

#region main function
if __name__ == '__main__':
    # attempt to load session from file
    if os.path.isfile(SAVEFILE_NAME):
        load_session_from_file(SAVEFILE_NAME)
    quit = False
    while not quit:
        # read stdin
        raw_str = input(f'{SCRIPT_NAME}> ')
        # process raw stdin
        tokenized_input = raw_str.strip().split()
        if len(tokenized_input) <= 0:
            continue
        # extract commands/args
        command = tokenized_input[0]
        arguments = tokenized_input[1:]
        arg_count = len(arguments)
        is_invalid_command = False
        invalid_command_reason = ''
        # process commands
        if command in EXIT_COMMANDS:
            quit = True
            continue
        elif command in INFO_COMMANDS:
            display_employees()
        elif command in LIST_COMMANDS:
            display_employees()
        elif command in ADD_COMMANDS:
            if arg_count < 1:
                is_invalid_command = True
                invalid_command_reason = f'command requires at least 1 argument'
            elif arguments[0] in EMPLOYEE_KEYWORDS:
                add_employees()
            else:
                is_invalid_command = True
                invalid_command_reason = f'unknown argument "{arguments[0]}"'
        elif command in REMOVE_COMMANDS:
            if arg_count < 1:
                is_invalid_command = True
                invalid_command_reason = f'command requires at least 1 argument'
            elif arguments[0] in EMPLOYEE_KEYWORDS:
                remove_employees()
            else:
                is_invalid_command = True
                invalid_command_reason = f'unknown argument "{arguments[0]}"'
        elif command in SET_COMMANDS:
            if arguments[0] in HOUR_KEYWORDS:
                set_tippable_hrs()
            else:
                is_invalid_command = True
                invalid_command_reason = f'unknown argument "{arguments[0]}"'
        else:
            is_invalid_command = True
            invalid_command_reason = f'command not found "{command}"'
        # print invalid command message
        if is_invalid_command:
            print('Invalid command: ' + invalid_command_reason)
    # save session to file
    save_session_to_file(SAVEFILE_NAME)
#endregion