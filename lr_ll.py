#tokenize functions to format file contents to be used properly
def tokenize_line(line):
  instruction = line.replace(" ", "")
  instruction = instruction.replace("\n", "")
  instruction = instruction.split(";")
  return instruction

def tokenize(str):
  tokens = []
  current_token = ""
  for char in str:
      if char.isalpha():
        current_token += char
      elif char.isdigit():
        current_token += char
      elif char in "+*()$":
        if current_token:
          tokens.append(current_token)
          current_token = ""
        tokens.append(char)
  if current_token:
    tokens.append(current_token)
  return tokens


#The function that prints ll table's rows
def ll_table(no, stack,input):
  stack_string = "".join(stack) #turns stack into string
  input_string = "".join(input)#turns input stack into string
  #if there is a action according to parsing table
  if stack[-1] in grammer_ll and input[0] in grammer_ll[stack[-1]]:
      action = grammer_ll[stack[-1]][input[0]]
      action_string = stack[-1] + "->" + "".join(action)
  else:#if there is not prints the invalid message
      if stack_string == input_string:
        action_string = "ACCEPT"
      else:
        action_string = "Rejected (" + stack[-1]+ " does not have an action/step for " + input[0]
  row = "| {:^5} | {:^10} | {:^10} | {:^10} |".format(str(no), stack_string, input_string, action_string)#formats the row
  print(row)
  
#prints the lr table's rows
def lr_table(no, stack,read,input):
  stack_string = " ".join(str(i) for i in stack)#turns stack into string
  input_string = "".join(input)#turns input into string
  stack_top = str(stack[-1])

  #if there is a action for stack's top element
  if stack_top in grammer_lr and read in grammer_lr[stack_top]:
    if '->' in grammer_lr[stack_top][read]:
      action_string = "Reverse " + grammer_lr[stack[-1]][read]
    elif 'State' in grammer_lr[stack_top][read]:
      action = grammer_lr[stack_top][read].replace("State_", "")
      action_string = "Shift to state " + action
    else:
      action_string = "ACCEPT"
  else:
    action_string = "Rejected (State " + stack_top+ " does not have an action/step for " + read
  row = "| {:^5} | {:^10} | {:^10} | {:^10} | {:^20} |".format(no, stack_string, read, input_string, action_string)
  print(row)


#LL function
def parse_string(input):
  stack =['$', 'E']#added E because it is always the first non-terminal
  input = tokenize(input)#tokenizes input
  header = "| {:^5} | {:^10} | {:^10} | {:^10} |".format("NO", "STACK", "INPUT", "ACTION")
  print(header)
  print("-" * len(header))
  i = 1
  ll_table(i, stack, input)
  while stack:
      i += 1
      top_symbol = stack[-1]#gets the stack's top
      next_input_symbol = input[0]#gets the inputs first
      if top_symbol == next_input_symbol:#if there is a match deletes it from stack and input
          if top_symbol == '$':#if there is $ at the top it means its accepted
              ll_table(i,stack,input)
              input.pop(0)
              stack.pop()
              break
          else:
              stack.pop()
              input.pop(0)
      elif top_symbol in grammer_ll and next_input_symbol in grammer_ll[top_symbol]:
        #if there is an action in non-terminal's terminal
        ll_table(i, stack, input)#prints the row
        stack.pop()#removes the top
        action = grammer_ll[top_symbol][next_input_symbol]#takes the action
        if action != ['ϵ']:#if action is not this symbol .. because this means pop
          reversed_list = action[::-1]#revereses the action in order to add it to stack
          stack.extend(reversed_list)#adds to stack
      else:
        break

#LR function
def parse_input(input):
  stack = [1]
  index = 0
  header = "| {:^5} | {:^10} | {:^10} | {:^10} | {:^20} |".format("NO", "STACK", "READ", "INPUT", "ACTION")
  print(header)
  print("-" * len(header))
  i = 1
  lr_table(i, stack, input[index], input)
  while stack:
    i += 1
    stack_top = str(stack[-1])
    if stack_top in grammer_lr and input[index] in grammer_lr[stack_top]:
      if 'Accept' in grammer_lr[stack_top][input[index]]:#accepted condition
        break;
      elif 'State' in grammer_lr[stack_top][input[index]]:#shift condition
        stack_input = grammer_lr[stack_top][input[index]].replace("State_", "")#takes the shift state
        stack.append(stack_input)#adds it to stack
        index += 1
      elif '->' in grammer_lr[stack_top][input[index]]:#reverse condition
        line = grammer_lr[stack_top][input[index]].split('->')
        back = len(line[1])
        forth = len(line[0])
        new_string = input[:index-back] + line[0] + input[index+forth-1:]#updates the input
        new_length = len(new_string)
        old_length = len(input)
        index = new_length - (old_length - index) - forth#updated index for reversed action
        input = new_string
        for j in range(back):#deletes the reversed indices
          stack.pop()
      lr_table(i, stack, input[index], input)
    else:
      break

grammer_lr = {}#parsing table for lr
with open("lr.txt", "r") as file:
    lines = file.readlines()
    length = len(lines)
    states = tokenize_line(lines[1])
    for i in range(2, length):
      line = tokenize_line(lines[i])
      length_line = len(line)
      nested_grammer_lr = {}
      for j in range(1, length_line):
         if line[j] != '':
          nested_grammer_lr[states[j]] = line[j]
      grammer_lr[line[0].replace("State_", "")] = nested_grammer_lr

grammer_ll = {}#ll parsing table
with open("ll.txt", "r") as file:
  lines = file.readlines()#reads the lines
  length = len(lines)
  LL = tokenize_line(lines[0])#tokenizes the first line to get terminals
  for i in range(1, length):#reads every line
    line = tokenize_line(lines[i])
    length_line = len(line)
    actions = {}#actions dictionary for the ith line
    for i in range(1, length_line):
      if line[i] != '':#if line is not empty
        line2 = line[i].split("->")
        tokens = list(line2[1])
        if 'i' in tokens:
          tokens.remove('i')
          tokens.remove('d')
          tokens.append('id')
        actions[LL[i]] = tokens
        grammer_ll[line[0]] = actions#adds it to non-terminals value as terminal acitons

#reads the input file and computes the funcitons
with open("input.txt", "r") as file2:
  input_lines = file2.readlines()
  length = len(input_lines)
  for i in range(1, length):
    input_line = tokenize_line(input_lines[i])
    if str(input_line[0]) == 'LL':
      parse_string(str(input_line[1]))
      print()
    elif str(input_line[0]) == "LR":
      parse_input(str(input_line[1]))
      print()
