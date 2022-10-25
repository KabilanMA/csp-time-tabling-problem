import sys
import copy
sys.setrecursionlimit(10000)

input_file_name = str(sys.argv[1]).strip()
output_file_name = str(sys.argv[2]).strip()

def accept(filename):
    with open(filename, 'r') as file:
        temp = file.read()
        lines = temp.split('\n')
        data = []
        for line in lines:
            if line!='':
                temp_list = line.split(',')
                checker = '' in temp_list
                while checker:
                    temp_list.remove('')
                    checker = "" in temp_list
                data.append(temp_list)
        
    return data

def output(filename, data):
    dataStr = ""
    for row in data:
        rowStr = ""
        for col in row:
            rowStr += col + ","
        else:
            rowStr = rowStr[:-1]
        dataStr += rowStr+'\n'
    else:
        dataStr = dataStr[:-1]
    
    with open(filename, 'w') as file:
        file.write(dataStr)


def backtracking(assignment, slots, depth):
    # true for final node in DFS
    if depth == len(assignment):
        return True
    # subs = [sub_name, type, available_sub_timeslot]
    # rooms = [room_names]
    
    global sub_lines
    global rooms
    
    subject = sub_lines[depth][0]
    available_subject_timeslot = sub_lines[depth][2:]
    category = sub_lines[depth][1]
    if category == "c":
        for slot in available_subject_timeslot:
            if not slots[slot]:
                assignment[depth] = [subject, slot, rooms[0]]
                slots[slot] = rooms[0]
                if backtracking(assignment, slots, depth+1):
                    return True
                else:
                    slots[slot] = None
                    assignment[depth] = [subject, None, None]
        else:
            return False
    
    elif category == 'o':
        for slot in available_subject_timeslot:
            if not slots[slot]:
                assignment[depth] = [subject, slot, rooms[0]]
                slots[slot] = [rooms[0]]
                if backtracking(assignment, slots, depth+1):
                    return True
                else:
                    slots[slot]=None
                    assignment[depth] = [subject,None,None]
            elif type(slots[slot]) == list:
                asRooms = slots[slot]
                temp = copy.deepcopy(asRooms)
                if len(asRooms) == len(rooms):
                    continue
                asRooms.append(rooms[len(asRooms)])
                assignment[depth] = [subject, slot, asRooms[-1]]
                slots[slot] = asRooms
                if backtracking(assignment, slots, depth+1):
                    return True
                else:
                    slots[slot] = temp
                    assignment[depth] = [subject, None, None]
        else:
            return False

sub_lines = accept(input_file_name)
rooms = sub_lines.pop()
slots={}
assignment=[]

# get the data for all the slots and all the subjects
for subject_data in sub_lines:
    for slot in subject_data[2:]:
        if slot not in slots and slot!='':
            slots[slot] = None
    assignment.append([subject_data[0], None, None])

# assignement contains all the details as [subject, time_slot, room]
result = backtracking(assignment, slots, 0)

if result:
    output(output_file_name, assignment)
    print('\n')
    for sub in assignment:
        print(sub)
    print('\n')
else:
    print("Couldn't find a solution")
