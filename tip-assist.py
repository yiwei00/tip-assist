from dataclasses import dataclass
# constants
SCRIPT_NAME = 'tip-assist'
EXIT_COMMANDS = set(['quit', 'exit'])
INFO_COMMANDS = set(['info'])
EMPLOYEE_KEYWORDS = set(['employee', 'employees'])

#region data classes
@dataclass
class employee_t:
    last_name: str
    first_name: str
    middle_initial: str = ''
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
employees = []
tips = []

def display_employees():
    for i, employee in enumerate(employees):
        print(f'{i + 1:>2}. {employee.last_name[:9] + ",":<10} {employee.first_name:<10}')

# command to add employee
def add_employees():
    print('Existing employees: ')
    display_employees()
    print('Enter new employee name in the format of "last,first"')
    print('or enter "done" to finish')
    done = False
    # loop to add employees
    while not done:
        raw_name_str = input('> ')
        tokenized_name = raw_name_str.strip().split(',')
        if tokenized_name[0] == 'done':
            done = True
        elif len(tokenized_name) != 2:
            print('INVALID NAME FORMAT')
        else:
            employees.append(employee_t(
                last_name= tokenized_name[0].strip(),
                first_name=tokenized_name[1].strip()
            ))
    # sort employees via last name
    employees.sort(key=lambda e: e.last_name)

def remove_employees():
    done = False
    while not done:
        print('Employee list: ')
        display_employees()
        print('Enter the employee number to remove')
        print('or "done" to finish')
        is_invalid_command = False
        raw_str = input('> ')
        tokenized_input = raw_str.strip().split()
        if tokenized_input[0] == 'done':
            done = True
        elif tokenized_input[0].isdigit():
            employee_index = int(tokenized_input[0]) - 1
            if employee_index >= 0 and employee_index < len(employees):
                employees.pop(employee_index)
            else:
                is_invalid_command = True
        else:
            is_invalid_command = True
        if is_invalid_command:
            print('INVALID EMPLOYEE INDEX')

# main
if __name__ == '__main__':
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
        is_invalid_command = False
        # process commands
        if command in EXIT_COMMANDS:
            quit = True
            continue
        elif command in INFO_COMMANDS:
            display_employees()
        elif command == 'add':
            if arguments[0] in EMPLOYEE_KEYWORDS:
                add_employees()
            else:
                is_invalid_command = True
        elif command == 'remove':
            if arguments[0] in EMPLOYEE_KEYWORDS:
                remove_employees()
            else:
                is_invalid_command = True
        else:
            is_invalid_command = True
        # detecting invalid commands
        if is_invalid_command:
            print('Invalid command')
