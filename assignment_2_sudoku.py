from operator import itemgetter
from itertools import combinations

class SudokuError(Exception):
    def __init__(self, message):
        self.message = message

class Sudoku():
    def __init__(self, filename):
        self.filename = filename
        with open(self.filename) as input_data:
            data = input_data.read()
            data_list = []
            for smth in data:
                if smth.isdigit():
                    data_list.append(smth)
            if len(data_list) != 81:
                raise SudokuError('Incorrect input')
        #print(data_list)
        self.sudoku_lists = []
        temp_list = []
        for smth in data_list:
            #print(smth)
            temp_list.append(smth)
            #print(temp_list)
            if len(temp_list) == 9:
                self.sudoku_lists.append(list(temp_list))
                del temp_list[:]
                
        #creating columnview
        self.columnview = []
        for columns in reversed(range(9)):
            acolumn = []
            for rows in range(0, 9):
                acolumn.append(self.sudoku_lists[rows][columns])
            self.columnview.append(acolumn)
        
        #grouping the boxes
        box_ind = {1: (0,3,0,3), 2: (3,6,0,3), 3: (6,9,0,3), 4: (0,3,3,6),\
                   5: (3,6,3,6), 6: (6,9,3,6), 7: (0,3,6,9), 8:(3,6,6,9), 9: (6,9,6,9)}
        self.boxesview = []
        for nb in box_ind.keys():
            xfrom, xto, yfrom, yto = box_ind[nb]
            boxes = []
            for _rows in self.sudoku_lists[yfrom:yto]:
                for _columns in _rows[xfrom:xto]:
                    boxes.append(_columns)
            self.boxesview.append(boxes)
        #print(boxesview)
        
        #print(self.sudoku_lists)
        #print(self.columnview)
        
    def preassess(self):
        #checking row
        for _row in self.sudoku_lists:
            #checking using set
            lenwozero = len(_row) - (_row.count('0'))
            rowset =  set(_row)
            if (len(rowset)-1) != lenwozero:
                print('There is clearly no solution')
                return
                
        #checking column
        for _column in self.columnview:
            lenwozero = len(_column) - (_column.count('0'))
            columnset = set(_column)
            if (len(columnset)-1) != lenwozero:
                print('There is clearly no solution')
                return
            
        #checking boxes
        for _box in self.boxesview:
            lenwozero = len(_box) - (_box.count('0'))
            boxset = set(_box)
            if (len(boxset)-1) != lenwozero:
                print('There is clearly no solution')
                return
        print('There might be a solution')
        return
        
    def creatingfile(self, filetype, sudokulist):
        thefile =self.filename[:8] + '_' + filetype + '.tex'
        with open(thefile, 'w+') as afile:
            content = r"""\documentclass[10pt]{article}
\usepackage[left=0pt,right=0pt]{geometry}
\usepackage{tikz}
\usetikzlibrary{positioning}
\usepackage{cancel}
\pagestyle{empty}
    
\newcommand{\N}[5]{\tikz{\node[label=above left:{\tiny #1},
                                label=above right:{\tiny #2},
                                label=below left:{\tiny #3},
                                label=below right:{\tiny #4}]{#5};}}
    
\begin{document}
    
\tikzset{every node/.style={minimum size=.5cm}}
    
\begin{center}
\begin{tabular}{||@{}c@{}|@{}c@{}|@{}c@{}||@{}c@{}|@{}c@{}|@{}c@{}||@{}c@{}|@{}c@{}|@{}c@{}||}\hline\hline"""
            afile.write(content)
            for nb in range(9):
                content_head = '\n% Line ' + str(nb+1) +'\n'
                afile.write(content_head)
                for nb_ in range(9):
                    fill =  '' if sudokulist[nb][nb_] == str(0) else str(sudokulist[nb][nb_])
                    main_content = '\\N{}{}{}{}{' + fill +'} '
                    afile.write(main_content)
                    if nb_+1 == 9:
                        afile.write('\\\\ \hline')
                        if (nb+1) % 3 == 0:
                            afile.write('\hline')
                    else:
                        afile.write('& ')
                    if (nb_+1) % 3 == 0:
                        if (nb+1) == 9 and (nb_+1) == 9:
                            break
                        afile.write('\n')
            afile.write("\n\end{tabular}\n\end{center}\n\n\end{document}")
    
    def bare_tex_output(self):
        self.creatingfile('bare', self.sudoku_lists)
        return
    
    def forced_tex_output(self):
        self.finaloutput = list(self.sudoku_lists)
        self.newcolumnview = list(self.columnview)
        self.newboxview = list(self.boxesview)
        #print(finaloutput)
        #Find numbers in sudoku
        set_nb = set()
        for rowlist in self.finaloutput:
            newset = set(rowlist)
            set_nb = set_nb | newset
            
        #to delete 0 from the set
        set_nb = set_nb ^ {'0'}
        
        #counting each of the number, the result recorded in list of tuples
        nb_count = []
        for nb in set_nb:
            #print(nb)
            total = 0
            for rowlist in self.finaloutput:
                if nb in rowlist:
                    total += 1
            nb_count.append((nb,total))
        
        #sorting the list from big to small according to the 2nd value of tuples
        nb_count = sorted(nb_count, key= itemgetter(1), reverse = True)
        
        #find box that doesn't have the number yet
        repeat = True
        while repeat:
            repeat = False
            for biggestnb in nb_count:
                #print('biggestnb', biggestnb)
                ok_box = []
                for boxrow in self.newboxview:
                    if boxrow.count(biggestnb[0]) == 0:
                        ok_box.append(self.newboxview.index(boxrow))
                
                #check per allowed box
                box_ind = {1: (0,3,0,3), 2: (3,6,0,3), 3: (6,9,0,3), 4: (0,3,3,6),\
                   5: (3,6,3,6), 6: (6,9,3,6), 7: (0,3,6,9), 8:(3,6,6,9), 9: (6,9,6,9)}
                for boxind in ok_box:
                    xfrom, xto, yfrom, yto = box_ind[boxind+1]
                    rowbreak = False
                    candidate = []
                    for rowind in range(yfrom, yto):
                        for colind in range(xfrom, xto):
                            if self.finaloutput[rowind][colind] == '0':
                                #check row
                                if biggestnb[0] in self.finaloutput[rowind]:
                                    continue
                                #check column
                                if biggestnb[0] in self.newcolumnview[8-colind]:
                                    continue
                                #record cell
                                candidate.append((rowind,colind))
                                if len(candidate) > 1:
                                    rowbreak = True
                                    break                                    
                        if rowbreak:
                            break
                    if len(candidate) == 1:
                        repeat = True
                        self.finaloutput[candidate[0][0]][candidate[0][1]] = biggestnb[0]
                        self.newcolumnview[8-candidate[0][1]][candidate[0][0]] = biggestnb[0]
                        
                #inputting the boxupdate
                self.newboxview = []
                for nb in box_ind.keys():
                    xfrom, xto, yfrom, yto = box_ind[nb]
                    boxes = []
                    for _rows in self.finaloutput[yfrom:yto]:
                        for _columns in _rows[xfrom:xto]:
                            boxes.append(_columns)
                    self.newboxview.append(boxes) 

        self.creatingfile('forced', self.finaloutput)
        return
    
    def marked_tex_output(self):
        self.forced_tex_output()
        self.markedlist = list(self.finaloutput)
        self.markedcol = list(self.columnview)
        self.markedbox = list(self.newboxview)
        self.markedsudoku = []
        thefile =self.filename[:8] + '_marked.tex'       
        with open(thefile, 'w+') as afile:
            content = r"""\documentclass[10pt]{article}
\usepackage[left=0pt,right=0pt]{geometry}
\usepackage{tikz}
\usetikzlibrary{positioning}
\usepackage{cancel}
\pagestyle{empty}
    
\newcommand{\N}[5]{\tikz{\node[label=above left:{\tiny #1},
                                label=above right:{\tiny #2},
                                label=below left:{\tiny #3},
                                label=below right:{\tiny #4}]{#5};}}
    
\begin{document}
    
\tikzset{every node/.style={minimum size=.5cm}}
    
\begin{center}
\begin{tabular}{||@{}c@{}|@{}c@{}|@{}c@{}||@{}c@{}|@{}c@{}|@{}c@{}||@{}c@{}|@{}c@{}|@{}c@{}||}\hline\hline"""
            afile.write(content)   
            for rowind in range(0,9):
                content_head = '\n% Line ' + str(rowind+1) +'\n'
                afile.write(content_head)
                tempsudoku = []
                for colind in range(0,9):
                    afile.write('\\N')
                    if self.markedlist[rowind][colind] == '0':
                        #print(f'rowind {rowind}, colind {colind}')
                        rowval = set(self.markedlist[rowind])
                        colval = set(self.markedcol[8-colind])
                        boxnb = ((rowind//3)*3)+(colind//3)
                        boxval = set(self.markedbox[boxnb])
                        #print(f'rowval {rowval}, colval {colval}, boxval {boxval}')
                        fullset = (rowval | colval | boxval) ^ set('0') ^ set(['1', '2', '3', '4', '5', '6', '7' , '8', '9'])
                        tempsudoku.append(fullset)
                        #print(fullset)
                        
                        count = 0
                        for nb in range(0,4):
                            count += 1
                            afile.write('{')
                            
                            if nb == 3:
                                filla = str(nb+count) if str(nb+count) in fullset else ''
                                fillb = str(nb+count+1) if str(nb+count+1) in fullset else ''
                                fillc = str(nb+count+2) if str(nb+count+2) in fullset else ''
                                between1 = ' ' if filla != '' and (fillb != '' or fillc != '') else ''
                                between2 = ' ' if fillc != '' and fillb != '' else ''
                                fill = filla + between1 + fillb + between2 + fillc  
                                #print(fill)
                            else:
                                #if str(nb+count) in fullset:
                                #    print('works')
                                #else:
                                #    print('not working')
                                filla = str(nb+count) if str(nb+count) in fullset else ''
                                fillb = str(nb+count+1) if str(nb+count+1) in fullset else ''
                                #print('nb1', (nb+1))
                                #print('nb2', (nb+2))
                                #if (nb+count) in fullset and (nb+count+1) in fullset:
                                between = ' ' if filla != '' and fillb != '' else ''
                                fill = filla + between + fillb
                                #print(fill)
                                
                            afile.write(str(fill))
                            afile.write('}')
                        afile.write('{}')
                    else:
                        fill = str(self.markedlist[rowind][colind])
                        tempsudoku.append(fill)
                        main_content = '{}{}{}{}{' + fill +'}'
                        afile.write(main_content)
                    
                    if colind == 8:
                        afile.write('\\\\ \hline')
                    else:
                        afile.write('  & ')
                    if (colind+1) % 3 == 0:
                        afile.write('\n ')
                self.markedsudoku.append(tempsudoku)
                if (rowind+1) % 3 == 0:
                    afile.write('\hline\n')
            afile.write("\n\end{tabular}\n\end{center}\n\n\end{document}")
        #checking the result
        #for lists in self.markedsudoku:
        #    print(lists)
        #print('\n\n') 
        #for lists in boxchecklist:
        #    print(lists)        
    
    def canceling(self, value, row, column):
        cnvalue = set(value)
        cnrow = row
        cncolumn = column
        boxset = {1: (0,0), 2:(0,3), 3:(0,6), 4: (3,0), \
                  5: (3,3), 6: (3,6), 7:(6,0), 8: (6,3), 9:(6,6)}
        #checking row
        for colnb in range(9):
            if type(self.marked[cnrow][colnb]) == set:
                if self.marked[cnrow][colnb] & cnvalue == cnvalue:
                    self.cancelsudoku[cnrow][colnb] = self.cancelsudoku[cnrow][colnb] | cnvalue
                    self.marked[cnrow][colnb] = self.marked[cnrow][colnb] ^ cnvalue
                    self.markedcolumn[8-colnb][cnrow] = self.marked[cnrow][colnb]
                    boxnb = ((cnrow//3)*3)+(colnb//3)
                    boxcol = (cnrow+1)%3+((colnb%3)*3)
                    self.markedboxes[boxnb][boxcol] =self.marked[cnrow][colnb]
                    if len(self.marked[cnrow][colnb]) == 1:
                        self.cancelsudoku[cnrow][colnb] = self.cancelsudoku[row][col_] | self.marked[cnrow][colnb]
                        changes = list(self.marked[cnrow][colnb])
                        self.workedlist[cnrow][colnb] = changes[0]
                        #if workedcol and box used, change it as well
                        self.canceling(changes, cnrow, colnb)
        
        #checking col
        for rownb in range(9):
            if type(self.markedcolumn[8-cncolumn][rownb]) == set:
                if self.markedcolumn[8-cncolumn][rownb] & cnvalue == cnvalue:
                    self.cancelsudoku[rownb][cncolumn] = self.cancelsudoku[rownb][cncolumn] | cnvalue 
                    self.marked[rownb][cncolumn] = self.marked[rownb][cncolumn] ^ cnvalue
                    self.markedcolumn[8-cncolumn][rownb] = self.marked[rownb][cncolumn]
                    boxnb = ((rownb//3)*3)+(cncolumn//3) #ifwrong just + 1
                    boxcol = (rownb+1)%3+((cncolumn%3)*3)
                    self.markedboxes[boxnb][boxcol] =self.marked[rownb][cncolumn]
                    if len(self.markedcolumn[8-cncolumn][rownb]) == 1:
                        self.cancelsudoku[rownb][cncolumn] = self.cancelsudoku[rownb][cncolumn] | \
                        self.markedcolumn[8-cncolumn][rownb]
                        changes = list(self.markedcolumn[8-cncolumn][rownb])
                        self.workedlist[rownb][cncolumn] = changes[0]
                        #if workedcol and box used, change it as well
                        self.canceling(changes, rownb, cncolumn)
        
        #checking box
        boxnb = ((cnrow//3)*3)+(cncolumn//3)
        for boxind in range(9):
            if type(self.markedboxes[boxnb][boxind]) == set:
                if self.markedboxes[boxnb][boxind] & cnvalue == cnvalue:
                    rowind, colind = boxset[boxnb]
                    rowind = rowind + (boxind%3)
                    colind = colind + (boxind//3)
                    self.cancelsudoku[rowind][colind] = self.cancelsudoku[rowind][colind] | cnvalue 
                    self.marked[rowind][colind] = self.marked[rowind][colind] ^ cnvalue
                    self.markedcolumn[8-colind][rowind] = self.marked[rowind][colind]
                    self.markedboxes[boxnb][boxind] = self.marked[rowind][colind]
                    if len(self.markedboxes[boxnb][boxind]) == 1:
                        self.cancelsudoku[rowind][colind] = self.cancelsudoku[rowind][colind] | \
                        self.markedbox[boxnb][boxind]
                        changes = list(self.markedboxes[boxnb][boxind])
                        self.workedlist[rowind][colind] = changes[0]
                        #if workedcol and box used, change it as well
                        self.canceling(changes, rownb, cncolumn)
        
                    

        
    
    def worked_tex_output(self):
        self.marked_tex_output()
        self.workedlist = list(self.markedlist)
        self.workedcol = list(self.markedcol)
        self.workedbox = list(self.markedbox)
        self.marked = list(self.markedsudoku)
        
        #creating column
        self.markedcolumn = []
        for columns in reversed(range(9)):
            acolumn = []
            for rows in range(0, 9):
                acolumn.append(self.marked[rows][columns])
            self.markedcolumn.append(acolumn)
            
        #creating box
        box_ind = {1: (0,3,0,3), 2: (3,6,0,3), 3: (6,9,0,3), 4: (0,3,3,6),\
                   5: (3,6,3,6), 6: (6,9,3,6), 7: (0,3,6,9), 8:(3,6,6,9), 9: (6,9,6,9)}
        self.markedboxes = []
        for nb in box_ind.keys():
            xfrom, xto, yfrom, yto = box_ind[nb]
            boxes = []
            for _rows in self.workedlist[yfrom:yto]:
                for _columns in _rows[xfrom:xto]:
                    boxes.append(_columns)
            self.markedboxes.append(boxes)
            
        self.cancelsudoku = [[set('0') for i in range(9)] for a in range(9)]
        thefile =self.filename[:8] + 'worked.tex'       
        with open(thefile, 'w+') as afile:
            content = r"""\documentclass[10pt]{article}
\usepackage[left=0pt,right=0pt]{geometry}
\usepackage{tikz}
\usetikzlibrary{positioning}
\usepackage{cancel}
\pagestyle{empty}
    
\newcommand{\N}[5]{\tikz{\node[label=above left:{\tiny #1},
                                label=above right:{\tiny #2},
                                label=below left:{\tiny #3},
                                label=below right:{\tiny #4}]{#5};}}
    
\begin{document}
    
\tikzset{every node/.style={minimum size=.5cm}}
    
\begin{center}
\begin{tabular}{||@{}c@{}|@{}c@{}|@{}c@{}||@{}c@{}|@{}c@{}|@{}c@{}||@{}c@{}|@{}c@{}|@{}c@{}||}\hline\hline"""
            afile.write(content)   
            numbers = {'1','2','3','4','5','6','7','8','9'}

            #checking per row
            for row in range(9):
                #finding the full set available
                fullset = numbers ^ set(self.workedlist[row]) ^ set('0')
                #finding possible combination of full set
                for loop in range(2,len(fullset)-1):
                    possiblesets = combinations(fullset, loop)
                    for set_ in possiblesets:
                        #print(set_)
                        nbofcell = 0
                        cellind = []
                        for col in range(9):
                            if type(self.marked[row][col]) == set:
                                if self.marked[row][col].issubset(set_):
                                    nbofcell += 1
                                    cellind.append(col)
                            else:
                                continue
                        if len(set_) == len(cellind):
                            preemptive = set(set_)
                            for col_ in range(9):
                                if type(self.marked[row][col_]) == set:
                                    if col_ in cellind:
                                        continue
                                    self.marked[row][col_] = self.marked[row][col_] ^ (preemptive & self.marked[row][col_])
                                    self.markedcolumn[8-col_][row] = selfmarked[row][col_]
                                    self.cancelsudoku[row][col_] = preemptive & self.marked[row][col_]
                                    #if the len of marked is 1, force it in
                                    if len(self.marked[row][col_]) == 1:
                                        self.cancelsudoku[row][col_] = self.cancelsudoku[row][col_] | self.marked[row][col_]
                                        changes = list(self.marked[row][col_])
                                        self.workedlist[row][col_] = changes[0]
                                        #if workedcol and box used, change it as well
                                        self.canceling(changes, row, col_)
            
            #checking column
            for col in range(9):
                #finding the full set available
                fullset = numbers ^ set(self.workedcol[col]) ^ set('0')
                #finding possible combination of full set
                for loop in range(2,len(fullset)-1):
                    possiblesets = combinations(fullset, loop)
                    for set_ in possiblesets:
                        #print(set_)
                        nbofcell = 0
                        cellind = []
                        for row in range(9):
                            if type(self.markedcolumn[col][row]) == set:
                                if self.markedcolumn[col][row].issubset(set_):
                                    nbofcell += 1
                                    cellind.append(row)
                            else:
                                continue
                        if len(set_) == len(cellind):
                            preemptive = set(set_)
                            for row_ in range(9):
                                if type(self.markedcolumn[col][row_]) == set:
                                    if row_ in cellind:
                                        continue
                                    self.markedcolumn[col][row_] = self.markedcolumn[row][col_] ^ (preemptive & self.marked[row][col_])
                                    self.markedcolumn[8-col_][row] = selfmarked[row][col_]
                                    self.cancelsudoku[row][col_] = preemptive & self.marked[row][col_]
                                    #if the len of marked is 1, force it in
                                    if len(self.marked[row][col_]) == 1:
                                        self.cancelsudoku[row][col_] = self.cancelsudoku[row][col_] | self.marked[row][col_]
                                        changes = list(self.marked[row][col_])
                                        self.workedlist[row][col_] = changes[0]
                                        #if workedcol and box used, change it as well
                                        self.canceling(changes, row, col_)
                                
                        
                    
    
        
                
        
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            

#sudoku = Sudoku('sudoku_5.txt')
#sudoku.preassess()
#sudoku.bare_tex_output()
#sudoku.forced_tex_output()
#sudoku.marked_tex_output()
#sudoku.worked_tex_output()