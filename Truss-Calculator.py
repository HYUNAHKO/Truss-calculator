import tkinter as tk
import tkinter.ttk as ttk
from math import*
import numpy as np

hinge_point = 0
roller_point = 0
hinge_point_format_of_pL = 0  #hinge point가 point_list의 몇 번째 index인지
roller_point_format_of_pL = 0 #roller point가 point_list의 몇 번째 index인지

display_size = (1400, 900) #가로(width) = 1400 픽셀 세로(height) = 900 픽셀

truss_connection = [] # ( , ) 들이 list 안에 같이 들어 있음.

point_list = [(0, 0)] #entry에 입력 후 point들이 저장되는 list

truss_force = []

force_list = [] #(index , force x, force y)

point_list_for_combo = [(0, 0)] #입력 후 combobox에 저장되는 point_list들


def draw_coordinates(coordinates): #점과 점들을 이어 canvas 를 이용해 그림으로 나타나게 하는 함수
    for connection in truss_connection:
        a, b = connection  
        xa, ya, xb, yb = point_list_for_display[a][0]+x_o_point,\
            -point_list_for_display[a][1]+y_o_point, point_list_for_display[b][0]+x_o_point, -point_list_for_display[b][1]+y_o_point
            #connection에서 두 점의 인덱스 'a'와 'b'에 할당. 

        canvas.create_line(xa, ya, xb, yb, fill='black', width=5) #선 색깔은 검은색, 너비는 5. tkinter 안의 canvas에서 Line 생성하게끔 함. 
    graph.mainloop() #GUI 이벤트 루프 실행하는 method. mainloop() method는 이벤트 루프를 시작해 창을 열고 이벤트들을 처리하며, user와 상호작용함.


'''마지막 코드 truss_connection_asking_window.mainloop() 전에 제시되는 x_o_point= 50 &  y_o_point=display_size[1]*0.9 는 x 좌표의 기준점, y 좌표의 기준점
   '''

def append_line(): #점과 점을 이어 트러스를 생성하는 함수
    a = combobox21.current() #current() 메서드는 선택된 옵션의 index를 가져옴. 점들의 인덱스 입력. 예를 들어, 1번 점과 2번 점을 연결하면, (1,2) 로 저장됨.
    b = combobox22.current() #combobx는 사용자에게 선택할 수 있는 목록을 제시하고, 그 중 하나를 선택하게 함.
    if a == b:
        label3 = tk.Label(truss_connection_asking_window, text="서로 다른 트러스를 선택하세요. ", fg="red") #tk.label을 통해 '문장' 위젯 생성
        label3.pack(side="top") # pack() method는 위젯을 화면에 배치하는 역할. side로 가능한 값 "top", "bottom" "left" "right"
        label3.after(1000, label3.destroy) # 'label3' 위젯을 생성한 후 1000ms(1초)가 지난 후 destroy() 메서드를 실행해 위젯을 제거.
    else:
        if a>b:
            _ = a
            a = b
            b = _ 
            '''truss connection에서 겹치는 경우 연결을 막기 위해 1box= a, 2box= b를 넣은 경우와
               1box= b, 2box= a를 넣은 경우가 같게, 
            a가 b보다 큰 경우, a와 b의 값을 교환해서 항상 b가 a보다 크게끔 저장.'''
        
        if (a, b) in truss_connection:
            label3 = tk.Label(truss_connection_asking_window, text="이미 연결한 트러스 입니다", fg="red")
            label3.pack(side="top")
            label3.after(1000, label3.destroy)
        else:
            truss_connection.append((a,b))  #튜플 형태로 truss connection list에 이를 저장함.
            draw_coordinates(point_list_for_display) 

class InvalidAngleError(Exception): #180도 이상의 값을 입력하면 Exception이 뜨게 하는 class 따로 지정.
    pass    

def append_point(): #user가 입력하는 값에 따라 점을 입력하는 함수
    previous_point = combobox1.current() #user가 연결을 시작할 점
    truss_length = entry11.get() #entry에서 user가 입력한 length, angle을 받도록 함.
    truss_angle = entry12.get() # get() 함수는 entry 에 입력된 텍스트값을 가져옴. 
    try:
        angle = float(truss_angle)
        if angle < 0 or angle > 180:
            raise InvalidAngleError
        x = cos(float(truss_angle)*pi/180)*float(truss_length) + point_list[previous_point][0] #x, y 변화량 계산
        y = sin(float(truss_angle)*pi/180)*float(truss_length) + point_list[previous_point][1]
        point_list.append((x, y)) 
        point_list_for_combo.append((round(x, 2), round(y, 2))) # 소수점 둘째 자리까지만 제시.
        new_point_into_combo = (round(x, 2), round(y, 2))
        combobox1['values'] += (new_point_into_combo),  # 선택지에 새로운 항목 추가
        entry11.delete(0, tk.END) #entry11, 12의 텍스트를 삭제. 0부터 tk.END 범위까지 모두 삭제한다는 의미.
        entry12.delete(0, tk.END) 
        label14 = tk.Label(window_asking_point_coordinate, text=(str(round(point_list[-1][0], 2)))+"  "+str(round(point_list[-1][1], 2))) #index [-1]->가장 최근 점, [0]=x 좌표, [1]=y 좌표
        label14.pack(side="top")  #window_asking_point_coordinate = tk.Tk() 윈도우 생성하기 위한 클래스
    except InvalidAngleError:
        label13 = tk.Label(window_asking_point_coordinate, text="0°~180° 사이의 값만 입력하세요", fg="red")
        label13.pack(side="top")
        label13.after(1000, label13.destroy)
    except ValueError:
        label13 = tk.Label(window_asking_point_coordinate, text="숫자만 입력하세요", fg="red")
        label13.pack(side="top")
        label13.after(1000, label13.destroy)


def append_F_point():
    global hinge_point #global - 해당 변수는 함수 외부에서도 접근 가능한 변수로 간주된다. 함수 내부에서 변수를 변경하면 외부에서도 유지됨.
    global roller_point
    global hinge_point_format_of_pL
    global roller_point_format_of_pL    
    hinge_point = point_list[combobox23.current()] # hinge 점 point_list에 저장.
    hinge_point_format_of_pL = combobox23.current() #hinge 점이 point_list의 몇 번째 index인지 변수에 저장.
    roller_point = point_list[combobox24.current()] # roller 점 point_list에 저장.
    roller_point_format_of_pL = combobox24.current() #roller 점이 point_list의 몇 번째 index인지 변수에 저장.
    canvas.create_polygon( hinge_point[0]*display_scale+x_o_point-10, - hinge_point[1]*display_scale+y_o_point+20, 
                        hinge_point[0]*display_scale+x_o_point+10, - hinge_point[1]*display_scale+y_o_point+20,
                        hinge_point[0]*display_scale+x_o_point, - hinge_point[1]*display_scale+y_o_point+7, fill='black', width=5)
    
    canvas.create_oval(roller_point[0]*display_scale+x_o_point-5, -roller_point[1]*display_scale+y_o_point+20, 
                       roller_point[0]*display_scale+x_o_point+5, -roller_point[1]*display_scale+y_o_point+10,
                        fill='black', width=5)  
    ''' polygon = hinge, oval = roller 에 대한 점의 좌표 제시. x_o_point, y_o_point는 기준점이고, 
    display_scale = 화면에 표시될 때 좌표 크기 조절. hinge(roller)_point[0] x좌표,  [1]은 y좌표이다. 
    -10, +20 등은 점들과 겹치지 않기 위해 x좌표, y좌표들을 이동시키고 도형을을 제시하기 위함. '''
    

def append_Force():
    
    force_point = point_list[combobox25.current()] #수동 입력, 연직 아래, 연직 위, 왼쪽, 오른쪽 중 선택 후 index 에 따라 point_list에서 해당 점 불러옴. 
    force_mode_var_result = force_mode_var.get()
    
    '''force_mode_var = tk.IntVar()->IntVar 클래스는 정수형 데이터를 저장하는 데 사용되는 Tkinter의 변수 클래스.
    force_mode_var 객체를 생성하고, force_mode_var.get() 메서드를 호출하여 해당 변수의 값을 가져옴.  get()<- IntVar 객체의 현재 값(정수)을 반환.'''

    print(force_mode_var_result)
    if force_mode_var_result == 2: #연직 아래
        x_force = 0
        y_force = -float(entry21.get())
    elif force_mode_var_result == 3: #연직 위
        x_force = 0
        y_force = float(entry21.get())
    elif force_mode_var_result == 4: #왼쪽 
        x_force = -float(entry21.get()) 
        y_force = 0
    elif force_mode_var_result == 5: #오른쪽
        x_force = float(entry21.get())
        y_force = 0
    elif force_mode_var_result == 1: #수동 입력
        x_force = cos(float(entry22.get())*pi/180)*float(entry21.get())
        y_force = sin(float(entry22.get())*pi/180)*float(entry21.get())

    force_list.append((combobox25.current(), x_force, y_force)) #index, x_force 힘, y_force 힘을 tuple 형태로 force_list에 저장.

    canvas.create_line(force_point[0]*display_scale+x_o_point, -force_point[1]*display_scale+y_o_point,
                        force_point[0]*display_scale+x_o_point+x_force/float(entry21.get())*50,
                        -force_point[1]*display_scale+y_o_point-y_force/float(entry21.get())*50,  fill='red', arrow=tk.LAST, width=3)
     
    force_text = str(abs(round(x_force, 2))) + "N  " + str(abs(round(y_force, 2))) + "N"
    canvas.create_text(force_point[0]*display_scale+x_o_point+x_force/float(entry21.get())*60,
                        -force_point[1]*display_scale+y_o_point-y_force/float(entry21.get())*60, text=force_text, fill=  "red" , font=("Arial", 10))

'''힘의 시작점인 force_point에서부터 x 방향으로 x_force/float(entry21.get())*50 만큼, y 방향으로 -y_force/float(entry21.get())*50 만큼 이동.
   canvas.create_text() 이 텍스트는 힘의 크기를 나타냄. str(round(x_force, 2)) + "N " + str(round(y_force, 2)) + "N" 형식으로 표시. '''    
 

def terminate_line_window():
    global trussforcematrix
    truss_connection_asking_window.destroy() #창을 닫으면 여태 입력한 point_list, truss_connection 등을 터미널에 print 해줌 
    print("point_list", point_list)
    print("truss_connection", truss_connection)
    print("force list", force_list)
    print("힌지", hinge_point_format_of_pL, hinge_point)
    print("롤러", roller_point_format_of_pL, roller_point)

    total_force_x, total_force_y = add_forces(force_list)  #add_forces function 실행한 force_list[(index, xforce1, yforce1)]
    hinge_momentum = 0
    for F in force_list: 
        hinge_momentum += F[2]*(point_list[F[0]][0]-hinge_point[0])-F[1]*(point_list[F[0]][1]-hinge_point[1])
    # for loop로 force_list 저장된 힘으로 hinge 모멘트 계산. 
    # 앞의 항은 x힘 요소(yforce*(pointlist에서 힘을 준 index의 x 좌표-hinge x좌표)). 
    # 뒤의 항은 y힘 요소(xforce*(pointlist에서 힘을 준 index의 y 좌표-hinge y좌표)).

    roller_force = -hinge_momentum/(roller_point[0]-hinge_point[0]) #roller_force =  - (힌지점에서의 모멘트의 합) / (롤러점과 힌지점 사이의 수평 거리)
    hinge_xforce = -total_force_x # hinge_xforce = -totat_force_x
    hinge_yforce = -total_force_y - roller_force # hinge_yforce = -(힌지점에서의 수직 힘의 합 + 롤러 힘)
    print("rf", roller_force,"hx", hinge_xforce, "hy", hinge_yforce)
    
    external_force_list = np.zeros((2*len(point_list), 1)) #point_list에 저장된 점들의 개수만큼 0으로 정한 외부 힘 벡터 external_force_list를 생성 & 행렬의 크기는 (2*len(point_list), 1)

    for F in force_list:
        external_force_list[F[0]*2][0] += -F[1] 
        external_force_list[F[0]*2+1][0] += -F[2]
    # external_force_list[F[0]*2][0]는 x 방향 힘을 나타내는 위치에 -F[1]을 더하여 외부 힘을 더함. 
    # external_force_list[F[0]*2+1][0]는 y 방향 힘을 나타내는 위치에 -F[2]를 더하여 외부 힘을 더함.
    external_force_list[hinge_point_format_of_pL*2][0] += -hinge_xforce
    external_force_list[hinge_point_format_of_pL*2+1][0] += -hinge_yforce
    external_force_list[roller_point_format_of_pL*2+1][0] += -roller_force
    #외력이 hinge x,y force & roller force에 작용하는 힘 더해줌.

    # truss_force_coefficent 행렬은 각 점과 트러스 구성원 사이의 관계를 나타내는 계수
    truss_force_coefficent = np.zeros((2*len(point_list), len(truss_connection))) # 행렬 (2*pointlist 길이Xtruss들의 길이)
    for i, tc in enumerate(truss_connection): #truss_connection 안에 있는 첫 번째 점-point1, 두 번째 점-point2 라고 하면,
        a = point_list[tc[0]][0]-point_list[tc[1]][0] #x축 차이
        b = point_list[tc[0]][1]-point_list[tc[1]][1] #y축 차이 
        fxc = a/sqrt(a**2+b**2) #x축 계수
        fyc = b/sqrt(a**2+b**2) #y축 계수 
        truss_force_coefficent[tc[0]*2][i] = fxc #point1의 x축 계수
        truss_force_coefficent[tc[0]*2+1][i] = fyc #point1의 y축 계수
        truss_force_coefficent[tc[1]*2][i] = -fxc #point2의 x축 계수
        truss_force_coefficent[tc[1]*2+1][i] = -fyc #point2의 y축 계수 

    
    trussforcematrix = np.linalg.pinv(truss_force_coefficent, rcond=1e-15, hermitian=False)@external_force_list

    #트러스 힘 계수 행렬과 외부 힘 벡터를 이용하여 트러스 힘 행렬 trussforcematrix를 계산하는 과정.
    # np.linalg.pinv() 함수를 사용하여 유사 역행렬을 계산한 후, 외부 힘 벡터와 행렬을 곱한다.

    a = trussforcematrix.tolist()  #Python의 리스트 형식으로 변환하여 a에 할당합니다.

    for tf in (trussforcematrix.tolist()):
        truss_force.append(-tf[0])
    # trussforcematrix에 저장된 각 트러스 힘 값을 음수로 취하고, truss_force 리스트에 추가 
    # 각 트러스의 힘은 리스트에 단일 요소로 추가됩니다    
    
    print(truss_force)
    
    showing_result()
    
    canvas.create_line(hinge_point[0]*display_scale+x_o_point-100, -hinge_point[1]*display_scale+y_o_point, hinge_point[0]*display_scale+x_o_point-10, -hinge_point[1]*display_scale+y_o_point, fill='green', arrow=tk.LAST, width=5)
    canvas.create_line(hinge_point[0]*display_scale+x_o_point, -hinge_point[1]*display_scale+y_o_point+100, hinge_point[0]*display_scale+x_o_point, -hinge_point[1]*display_scale+y_o_point+10, fill='green', arrow=tk.LAST, width=5)
    canvas.create_line(roller_point[0]*display_scale+x_o_point, roller_point[1]*display_scale+y_o_point+100, roller_point[0]*display_scale+x_o_point, roller_point[1]*display_scale+y_o_point+10, fill='green', arrow=tk.LAST, width=5)
    hinge_text_x = str(hinge_xforce) + "N" 
    hinge_text_y = str(hinge_yforce) + "N"
    roller_text = str(roller_force) + "N"
    canvas.create_text(hinge_point[0]*display_scale+x_o_point-150, -hinge_point[1]*display_scale+y_o_point, text=hinge_text_x, fill="black", font=("Arial", 10))
    canvas.create_text(hinge_point[0]*display_scale+x_o_point, -hinge_point[1]*display_scale+y_o_point+150, text=hinge_text_y, fill="black", font=("Arial", 10))
    canvas.create_text(roller_point[0]*display_scale+x_o_point, roller_point[1]*display_scale+y_o_point+150, text=roller_text, fill="black", font=("Arial", 10))
    #hinge, roller에 대한 반력 tkinter 창에 표시. 


def add_forces(force_list): #total force list 저장하는 함수 
    total_force_x_list = []
    total_force_y_list = []

    for a in range(len(force_list)):
        total_force_x_list.append(force_list[a][1]) #force_list에서 x축 방향으로 가해지는 힘들을 더함.
        total_force_y_list.append(force_list[a][2]) #force_list에서 y축 방향으로 가해지는 힘들을 더함.

    total_force_x = sum(total_force_x_list) 
    total_force_y = sum(total_force_y_list)

    return total_force_x,total_force_y    

def showing_result():  # 각 부재력의 인장력, 압축력을 보여주는 창
    for i, F in enumerate(truss_force):
        a, b = truss_connection[i]  # i 번 째 트러스의 연결 점(ex. 1번 점과 2번 점을 연결하면 (1,2)로 저장됨.)을 변수 a, b로 받음.
        xa, ya, xb, yb = point_list_for_display[a][0] + x_o_point, -point_list_for_display[a][1] + y_o_point, \
                         point_list_for_display[b][0] + x_o_point, -point_list_for_display[b][1] + y_o_point
        if F > 0:  # 인장력 (+), (xa, ya)에서 (xb, yb)까지 파란색으로 선을 그림. -10은 간격 조정 & 소수점 둘째 자리까지만 표시.
            canvas.create_line(xa, ya, xb, yb, fill='blue', width=5)
            canvas.create_text((xa + xb) // 2 - 10, (ya + yb) // 2 - 10, text="{인장력}\n" + str(round(F, 2)) + "N",
                               fill="green", font=("Arial", 15))

        elif F < 0:  # 압축력 (-), (xa, ya)에서 (xb, yb)까지 초록색으로 선을 그림.
            canvas.create_line(xa, ya, xb, yb, fill='red', width=5)
            canvas.create_text((xa + xb) // 2 - 10, (ya + yb) // 2 - 10, text="{압축력}\n" + str(round(-F, 2)) + "N",
                               fill="green", font=("Arial", 15))

def on_mouse_wheel(event):
    # 마우스 휠 처리
    if event.delta > 0:
        canvas.scale("all", event.x, event.y, 1.1, 1.1)
    else:
        canvas.scale("all", event.x, event.y, 0.9, 0.9)     
       

def terminate_point_window():
    window_asking_point_coordinate.destroy()
    print(point_list_for_combo, "com")
    print(point_list)  #window 창 종료 시 point_list_for_combo와 point_list가 터미널에 제시되도록 함.        

#window 창 1
window_asking_point_coordinate = tk.Tk() #창 형성
window_asking_point_coordinate.geometry("640x480") #크기



#label(글씨)와 입력 받을 combobox의 entry 상태, 크기 설정
label10 = tk.Label(window_asking_point_coordinate, text="기준점의 위치를 입력하세요\n (초기값은 0.0)" )
label10.pack(side="top")
combobox1 = ttk.Combobox(values = point_list, width=27) #values는 Combobox에 표시될 옵션 목록
combobox1.pack(side="top")

label11 = tk.Label(window_asking_point_coordinate, text="기준점과 입력하고자 하는 점 사이의 거리를 입력하세요" )
label11.pack(side="top")
entry11 = tk.Entry(window_asking_point_coordinate, width="5")
entry11.pack(side="top")

label12 = tk.Label(window_asking_point_coordinate, text="기준 점과 그리고자 하는 점의 각도를 입력하세요.  \n (방향은 x축 양의 방향에서 반시계 방향)" )
label12.pack(side="top")
entry12 = tk.Entry(window_asking_point_coordinate, width="5")
entry12.pack(side="top")

button11 = tk.Button(window_asking_point_coordinate, text= "추가", command=append_point) #버튼 누르면 함수 실행
button11.pack(side="top")

button12 = tk.Button(window_asking_point_coordinate, text= "다음", command=terminate_point_window) #창 종료
button12.pack(side="top")

label14 = tk.Label(window_asking_point_coordinate, text=("입력된 점의 위치\n0.0"))
label14.pack(side="top")


window_asking_point_coordinate.mainloop()

#window 창 2
truss_connection_asking_window = tk.Tk() #창 형성
truss_connection_asking_window.geometry("340x700") #크기 

label21 = tk.Label(truss_connection_asking_window, text="<트러스 연결 후 화면을 축소하시오.> \n 연결하고자 하는 첫번째 트러스를 입력하세요" )
label21.pack(side="top")
combobox21 = ttk.Combobox(values = point_list_for_combo, width=27)
combobox21.pack(side="top")


label22 = tk.Label(truss_connection_asking_window, text="연결하고자 하는 두번째 트러스를 입력하세요" )
label22.pack(side="top")
combobox22 = ttk.Combobox(values = point_list_for_combo, width=27)
combobox22.pack(side="top")


button21 = tk.Button(truss_connection_asking_window, text= "트러스 추가", command=append_line) #버튼 누르면 해당 함수 실행
button21.pack(side="top")

label23 = tk.Label(truss_connection_asking_window, text="힌지의 위치를 입력하세요" )
label23.pack(side="top")
combobox23 = ttk.Combobox(values = point_list_for_combo, width=27) #values는 Combobox에 표시될 옵션 목록, 크기 = 27
combobox23.pack(side="top")

label24 = tk.Label(truss_connection_asking_window, text="롤러의 위치를 입력하세요" )
label24.pack(side="top")
combobox24 = ttk.Combobox(values = point_list_for_combo, width=27) #values는 Combobox에 표시될 옵션 목록, 크기 = 27
combobox24.pack(side="top")

button22 = tk.Button(truss_connection_asking_window, text= "롤러, 힌지 추가", command=append_F_point) #버튼 누르면 해당 함수 실행
button22.pack(side="top")


#힘의 위치 추가

label25 = tk.Label(truss_connection_asking_window, text="힘의 위치를 입력하세요" )
label25.pack(side="top")

combobox25 = ttk.Combobox(values = point_list_for_combo, width=27)
combobox25.pack(side="top")


label26 = tk.Label(truss_connection_asking_window, text="힘의 크기를 입력하세요(N)" )
label26.pack(side="top")
entry21 = tk.Entry(truss_connection_asking_window, width="5")
entry21.pack(side="top")

force_mode_var = tk.IntVar()   #IntVAr() 클래스는 정수 값을 저장하는 Tkinter 변수 생성 
btn21 = tk.Radiobutton(truss_connection_asking_window, text="수동 입력", value=1, variable=force_mode_var)    #버튼 설정(truss_connection~.mainloop 실행되면), 텍스트 값, 변수, 이름(정수) 순
btn21.select() 
btn22 = tk.Radiobutton(truss_connection_asking_window, text="연직 아래로", value=2, variable=force_mode_var)
btn23 = tk.Radiobutton(truss_connection_asking_window, text="연직 위로", value=3, variable=force_mode_var)
btn24 = tk.Radiobutton(truss_connection_asking_window, text="왼쪽으로", value=4, variable=force_mode_var)
btn25 = tk.Radiobutton(truss_connection_asking_window, text="오른쪽으로", value=5, variable=force_mode_var)
btn21.pack() ; btn22.pack(); btn23.pack(); btn24.pack(); btn25.pack() #Tkinter의 pack() 메서드를 호출하여 해당 Radiobutton 위젯들을 화면에 표시하는 역할.

label25 = tk.Label(truss_connection_asking_window, text="힘의 각도를 표시하세요" )
label25.pack(side="top")
entry22 = tk.Entry(truss_connection_asking_window, width="5")
entry22.pack(side="top")

button23 = tk.Button(truss_connection_asking_window, text= "힘 추가", command=append_Force)
button23.pack(side="top")
button23 = tk.Button(truss_connection_asking_window, text= "다음", command=terminate_line_window)
button23.pack(side="top")

#트러스 그리는 창 
graph = tk.Tk()
canvas = tk.Canvas(graph, width=display_size[0], height=display_size[1])
canvas.pack()
canvas.bind("<MouseWheel>", on_mouse_wheel)

x_max = 0
y_max = 0
for p in point_list:
    if p[0] >= x_max:
        x_max = p[0]
    if p[1] >= y_max:
        y_max = p[1]
# point list에 있는 x, y 좌표 최댓값에 따라 display_scale을 결정하기 위함이다.

try:
    display_scale = min(display_size[0]*0.8/x_max, display_size[1]*0.8/y_max) #처음에 주어진 display_size에서 x, y 최댓값을 이용해 display_scale 변수 생성
except ZeroDivisionError:
    import tkinter as tk

    error_window = tk.Tk()
    error_window.title("Error")
    error_window.geometry("400x200")
    error_message = "주어진 점들로는 트러스를 형성할 수 없습니다."
    label = tk.Label(error_window, text=error_message, fg="red")
    label.pack()

    error_window.mainloop()
    # error message 띄운 후, script 나감.
    import sys
    sys.exit()

# 만약 entry에 입력한 점들의 y좌표가 전부 0인 경우 display 창 형성 불가능. 예외 처리함. 
# 이후 터미널에 NameError가 안 뜨게 하기 위해

# 화면에 점들을 표시하기 위한 point_list_for_display 설정
point_list_for_display = []
for pointtp in point_list:
    point_list_for_display.append((pointtp[0]*display_scale, 
                                   pointtp[1]*display_scale))
'''point_list에 있는 각 점들의 좌표값을 display_scale 값과 곱해 화면에 적절한 위치로 변환한 후,
 point_list_for_display 리스트에 추가함.'''

print(point_list_for_display)

#x_o_point, y_o_point은 각각 x, y 기준점에 따라 각 좌표값을 점들을 그림에 표시하고자 함.
x_o_point= 50
y_o_point=display_size[1]*0.9
for i, point in enumerate(point_list_for_display):
    canvas.create_oval(point[0]+x_o_point-1, -point[1]+y_o_point-1, 
                       point[0]+x_o_point+1, -point[1]+y_o_point+1,fill='black', width=5)
    point_text = str(round(point_list[i][0], 2)) + "  " + str(round(point_list[i][1], 2)) 
    canvas.create_text(point[0]+x_o_point-10, -point[1]+y_o_point-10, 
                       text=point_text, font=("Arial", 15))
truss_connection_asking_window.mainloop()


