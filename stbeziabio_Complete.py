import streamlit as st
import pandas as pd
import plotly.graph_objects as go

#ページ初期設定
st.set_page_config(page_title="環境分析",layout="wide",initial_sidebar_state="auto")

 #レイアウト設定 
layout_Ondo = go.Layout(title=dict(text='<b>【温度】'),
                    yaxis = dict(side = 'left',range = [0, 55]),
                    font=dict(size=15),
                    legend=dict(xanchor='left',
                    yanchor='bottom',
                    x=0.32,
                    y=1.0,
                    orientation='h'    
                    ),width=1350,height=550)
layout_Situdo = go.Layout(title=dict(text='<b>【相対湿度】'),
                    yaxis = dict(side = 'left',range = [0, 110]),
                    font=dict(size=15),
                    legend=dict(xanchor='left',
                    yanchor='bottom',
                    x=0.32,
                    y=1.0,
                    orientation='h'    
                    ),width=1350,height=550)
layout_Nisya = go.Layout(title=dict(text='<b>【日射】'),
                    yaxis = dict(side = 'left', range = [0,1100]),
                    font=dict(size=15),
                    legend=dict(xanchor='left',
                    yanchor='bottom',
                    x=0.32,
                    y=1.0,
                    orientation='h'    
                    ),width=1350,height=550)
layout_Co2 = go.Layout(title=dict(text='<b>【CO2濃度】'),
                    yaxis = dict(side = 'left', range = [0,1000]),
                    font=dict(size=15),
                    legend=dict(xanchor='left',
                    yanchor='bottom',
                    x=0.32,
                    y=1.0,
                    orientation='h'    
                    ),width=1350,height=550)
                            
#タイトル
st.title("環境分析")

# データフレーム読み込み
st.sidebar.write("""## ファイルアップロード""")
uploaded_file1 = st.sidebar.file_uploader("ファイル➀をアップロードしてください", type='csv',key=0)
with st.sidebar.expander("複数ファイルをアップロード"):
        # チェックが入っているときはデータフレームを書き出す
        uploaded_file2 = st.file_uploader("ファイル➁をアップロードしてください.", type='csv',key=1)
        uploaded_file3 = st.file_uploader("ファイル➂をアップロードしてください.", type='csv',key=2)

#表示グラフの切り替え
listgrafu = ['1.データ別4グラフ','2.相関2軸グラフ','3.近日比較グラフ','4.複数ファイルグラフ']
grafustock = st.selectbox(label="表示グラフを選択してください",options=listgrafu,key=3)

#1つ目のファイル読み込み
if uploaded_file1:
    df_readfile = pd.read_csv(uploaded_file1, encoding="shift-jis", index_col=[0], parse_dates=[0])
    df_changereadfile = df_readfile.reset_index()
    df_changereadfile = df_changereadfile.set_index("データ生成日時",drop=False)
    df_changereadfile.insert(1,"月日2",df_changereadfile["データ生成日時"].dt.strftime("%m月%d日"))

    #温室ごとに定義
    df_ex1 =  df_changereadfile[df_changereadfile["温室"] == 1]
    df_ex2 =  df_changereadfile[df_changereadfile["温室"] == 2]
    df_ex3 =  df_changereadfile[df_changereadfile["温室"] == 3]
    df_ex4 =  df_changereadfile[df_changereadfile["温室"] == 4]
    df_ex5 =  df_changereadfile[df_changereadfile["温室"] == 5]
    df_ex6 =  df_changereadfile[df_changereadfile["温室"] == 6]
    df_ex7 =  df_changereadfile[df_changereadfile["温室"] == 7]
    df_ex8 =  df_changereadfile[df_changereadfile["温室"] == 8]
    df_ex9 =  df_changereadfile[df_changereadfile["温室"] == 9]
    df_readfile1 = df_changereadfile

#2つ目のファイル読み込み
if uploaded_file2:
    df_readfile2 = pd.read_csv(uploaded_file2, encoding="shift-jis",index_col=[0],parse_dates=[0])
    df_changereadfile2 = df_readfile2.reset_index()
    df_changereadfile2 = df_changereadfile2.set_index("データ生成日時",drop=False)
    df_changereadfile2.insert(1,"月日2",df_changereadfile2["データ生成日時"].dt.strftime("%m月%d日"))
    df_readfile2 = df_changereadfile2
#3つ目のファイル読み込み
if uploaded_file3:
    df_readfile3 = pd.read_csv(uploaded_file3, encoding="shift-jis",index_col=[0],parse_dates=[0])
    df_changereadfile3 = df_readfile3.reset_index()
    df_changereadfile3 = df_changereadfile3.set_index("データ生成日時",drop=False)
    df_changereadfile3.insert(1,"月日2",df_changereadfile3["データ生成日時"].dt.strftime("%m月%d日"))
    df_readfile3 = df_changereadfile3

#===============データ別4グラフ=======================
if uploaded_file1 and '1.データ別4グラフ' in grafustock:
    #ヘッダー
    st.header("【温度・日射・相対湿度・CO2濃度のグラフ】")

    #サイドバーの日付選ぶ
    st.sidebar.write("""## 表示日付・温室選択""")
    select_dates = st.sidebar.date_input('表示日付の選択',value=(df_readfile1.index[-1],df_readfile1.index[-1]),min_value=df_readfile1.index[0],max_value=df_readfile1.index[-1])

    #温室番号選ぶ
    def sentaku():
        st.session_state["key"] = [1,2,3,4,5,6,7,8,9]
    list = sorted(set(df_readfile1['温室'].to_list()))
    stocks = st.sidebar.multiselect(label="温室番号の選択",
                options = list,
                default = list,
                key="key")
    all_sentaku = st.sidebar.button("全選択",on_click=sentaku)
    if not stocks:
        st.error('少なくとも1つの温室番号を選んでください。')

    #温室ごとグラフデータ定義
    ondofig = go.Figure(layout=layout_Ondo)
    situdofig = go.Figure(layout=layout_Situdo)
    nisyafig = go.Figure(layout=layout_Nisya)
    CO2fig = go.Figure(layout=layout_Co2)

    def process_1():
        selectday1 = df_ex1[select_dates[0].strftime("%Y-%m-%d"):select_dates[-1].strftime("%Y-%m-%d")]
        ondofig.add_traces(go.Scattergl(x=selectday1['データ生成日時'],
                                y=selectday1['温度'] ,
                                marker_color='dodgerblue',
                                line_width=1,
                                name='1',
                                yaxis='y1'))
        nisyafig.add_traces(go.Scattergl(x=selectday1['データ生成日時'],
                                y=selectday1['日射'] ,
                                marker_color='dodgerblue',
                                line_width=1,
                                name='1',
                                yaxis='y1'))
        situdofig.add_traces(go.Scattergl(x=selectday1['データ生成日時'],
                                y=selectday1['相対湿度'] ,
                                marker_color='dodgerblue',
                                line_width=1,
                                name='1',
                                yaxis='y1'))
        CO2fig.add_traces(go.Scattergl(x=selectday1['データ生成日時'],
                                y=selectday1['CO2濃度'] ,
                                marker_color='dodgerblue',
                                line_width=1,
                                name='1',
                                yaxis='y1'))
    def process_2():
        selectday2 = df_ex2[select_dates[0].strftime("%Y-%m-%d"):select_dates[-1].strftime("%Y-%m-%d")]
        ondofig.add_traces(go.Scattergl(x=selectday2['データ生成日時'],
                                y=selectday2['温度'] ,
                                marker_color='darkorange',
                                line_width=1,
                                name='2',
                                yaxis='y1'))
        nisyafig.add_traces(go.Scattergl(x=selectday2['データ生成日時'],
                                y=selectday2['日射'] ,
                                marker_color='darkorange',
                                line_width=1,
                                name='2',
                                yaxis='y1'))
        situdofig.add_traces(go.Scattergl(x=selectday2['データ生成日時'],
                                y=selectday2['相対湿度'] ,
                                marker_color='darkorange',
                                line_width=1,
                                name='2',
                                yaxis='y1'))
        CO2fig.add_traces(go.Scattergl(x=selectday2['データ生成日時'],
                                y=selectday2['CO2濃度'] ,
                                marker_color='darkorange',
                                line_width=1,
                                name='2',
                                yaxis='y1'))

    def process_3():
        selectday3 = df_ex3[select_dates[0].strftime("%Y-%m-%d"):select_dates[-1].strftime("%Y-%m-%d")]
        ondofig.add_traces(go.Scattergl(x=selectday3['データ生成日時'],
                                y=selectday3['温度'] ,
                                marker_color='mediumseagreen',
                                line_width=1,
                                name='3',
                                yaxis='y1'))
        nisyafig.add_traces(go.Scattergl(x=selectday3['データ生成日時'],
                                y=selectday3['日射'] ,
                                marker_color='mediumseagreen',
                                line_width=1,
                                name='3',
                                yaxis='y1'))
        situdofig.add_traces(go.Scattergl(x=selectday3['データ生成日時'],
                                y=selectday3['相対湿度'] ,
                                marker_color='mediumseagreen',
                                line_width=1,
                                name='3',
                                yaxis='y1'))
        CO2fig.add_traces(go.Scattergl(x=selectday3['データ生成日時'],
                                y=selectday3['CO2濃度'] ,
                                marker_color='mediumseagreen',
                                line_width=1,
                                name='3',
                                yaxis='y1'))
    def process_4():
        selectday4 = df_ex4[select_dates[0].strftime("%Y-%m-%d"):select_dates[-1].strftime("%Y-%m-%d")]
        ondofig.add_traces(go.Scattergl(x=selectday4['データ生成日時'],
                                y=selectday4['温度'] ,
                                marker_color='orangered',
                                line_width=1,
                                name='4',
                                yaxis='y1'))
        nisyafig.add_traces(go.Scattergl(x=selectday4['データ生成日時'],
                                y=selectday4['日射'] ,
                                marker_color='orangered',
                                line_width=1,
                                name='4',
                                yaxis='y1'))
        situdofig.add_traces(go.Scattergl(x=selectday4['データ生成日時'],
                                y=selectday4['相対湿度'] ,
                                marker_color='orangered',
                                line_width=1,
                                name='4',
                                yaxis='y1'))
        CO2fig.add_traces(go.Scattergl(x=selectday4['データ生成日時'],
                                y=selectday4['CO2濃度'] ,
                                marker_color='orangered',
                                line_width=1,
                                name='4',
                                yaxis='y1'))
    def process_5():
        selectday5 = df_ex5[select_dates[0].strftime("%Y-%m-%d"):select_dates[-1].strftime("%Y-%m-%d")]
        ondofig.add_traces(go.Scattergl(x=selectday5['データ生成日時'],
                                y=selectday5['温度'] ,
                                marker_color='mediumpurple',
                                line_width=1,
                                name='5',
                                yaxis='y1'))
        nisyafig.add_traces(go.Scattergl(x=selectday5['データ生成日時'],
                                y=selectday5['日射'] ,
                                marker_color='mediumpurple',
                                line_width=1,
                                name='5',
                                yaxis='y1'))
        situdofig.add_traces(go.Scattergl(x=selectday5['データ生成日時'],
                                y=selectday5['相対湿度'] ,
                                marker_color='mediumpurple',
                                line_width=1,
                                name='5',
                                yaxis='y1'))
        CO2fig.add_traces(go.Scattergl(x=selectday5['データ生成日時'],
                                y=selectday5['CO2濃度'] ,
                                marker_color='mediumpurple',
                                line_width=1,
                                name='5',
                                yaxis='y1'))
    def process_6():
        selectday6 = df_ex6[select_dates[0].strftime("%Y-%m-%d"):select_dates[-1].strftime("%Y-%m-%d")]
        ondofig.add_traces(go.Scattergl(x=selectday6['データ生成日時'],
                                y=selectday6['温度'] ,
                                marker_color='tan',
                                line_width=1,
                                name='6',
                                yaxis='y1'))
        situdofig.add_traces(go.Scattergl(x=selectday6['データ生成日時'],
                                y=selectday6['相対湿度'] ,
                                marker_color='tan',
                                line_width=1,
                                name='6',
                                yaxis='y1'))
        nisyafig.add_traces(go.Scattergl(x=selectday6['データ生成日時'],
                                y=selectday6['日射'] ,
                                marker_color='tan',
                                line_width=1,
                                name='6',
                                yaxis='y1'))
        CO2fig.add_traces(go.Scattergl(x=selectday6['データ生成日時'],
                                y=selectday6['CO2濃度'] ,
                                marker_color='tan',
                                line_width=1,
                                name='6',
                                yaxis='y1'))
    def process_7():
        selectday7 = df_ex7[select_dates[0].strftime("%Y-%m-%d"):select_dates[-1].strftime("%Y-%m-%d")]
        ondofig.add_traces(go.Scattergl(x=selectday7['データ生成日時'],
                                y=selectday7['温度'] ,
                                marker_color='hotpink',
                                line_width=1,
                                name='7',
                                yaxis='y1'))
        situdofig.add_traces(go.Scattergl(x=selectday7['データ生成日時'],
                                y=selectday7['相対湿度'] ,
                                marker_color='hotpink',
                                line_width=1,
                                name='7',
                                yaxis='y1'))
        nisyafig.add_traces(go.Scattergl(x=selectday7['データ生成日時'],
                                y=selectday7['日射'] ,
                                marker_color='hotpink',
                                line_width=1,
                                name='7',
                                yaxis='y1'))
        CO2fig.add_traces(go.Scattergl(x=selectday7['データ生成日時'],
                                y=selectday7['CO2濃度'] ,
                                marker_color='hotpink',
                                line_width=1,
                                name='7',
                                yaxis='y1'))
    def process_8():
        selectday8 = df_ex8[select_dates[0].strftime("%Y-%m-%d"):select_dates[-1].strftime("%Y-%m-%d")]
        ondofig.add_traces(go.Scattergl(x=selectday8['データ生成日時'],
                                y=selectday8['温度'] ,
                                marker_color='slategray',
                                line_width=1,
                                name='8',
                                yaxis='y1'))
        situdofig.add_traces(go.Scattergl(x=selectday8['データ生成日時'],
                                y=selectday8['相対湿度'] ,
                                marker_color='slategray',
                                line_width=1,
                                name='8',
                                yaxis='y1'))
        nisyafig.add_traces(go.Scattergl(x=selectday8['データ生成日時'],
                                y=selectday8['日射'] ,
                                marker_color='slategray',
                                line_width=1,
                                name='8',
                                yaxis='y1'))
        CO2fig.add_traces(go.Scattergl(x=selectday8['データ生成日時'],
                                y=selectday8['CO2濃度'] ,
                                marker_color='slategray',
                                line_width=1,
                                name='8',
                                yaxis='y1'))
    def process_9():
        selectday9 = df_ex9[select_dates[0].strftime("%Y-%m-%d"):select_dates[-1].strftime("%Y-%m-%d")]
        ondofig.add_traces(go.Scattergl(x=selectday9['データ生成日時'],
                                y=selectday9['温度'] ,
                                marker_color='rosybrown',
                                line_width=1,
                                name='9',
                                yaxis='y1'))
        situdofig.add_traces(go.Scattergl(x=selectday9['データ生成日時'],
                                y=selectday9['相対湿度'] ,
                                marker_color='rosybrown',
                                line_width=1,
                                name='9',
                                yaxis='y1'))
        nisyafig.add_traces(go.Scattergl(x=selectday9['データ生成日時'],
                                y=selectday9['日射'] ,
                                marker_color='rosybrown',
                                line_width=1,
                                name='9',
                                yaxis='y1'))
        CO2fig.add_traces(go.Scattergl(x=selectday9['データ生成日時'],
                                y=selectday9['CO2濃度'] ,
                                marker_color='rosybrown',
                                line_width=1,
                                name='9',
                                yaxis='y1'))
                                
    #温室選ばれた時の応答
    if 1 in stocks:
        process_1()
    if 2 in stocks:
        process_2()
    if 3 in stocks:
        process_3()
    if 4 in stocks:
        process_4()
    if 5 in stocks:
        process_5()
    if 6 in stocks:
        process_6()
    if 7 in stocks:
        process_7()
    if 8 in stocks:
        process_8()
    if 9 in stocks:
        process_9()


    #温度グラフ表示
    st.plotly_chart(ondofig)
    # #日射グラフ表示
    st.plotly_chart(nisyafig)
    # #相対湿度グラフ表示
    st.plotly_chart(situdofig)
    # #CO2濃度グラフ表示
    st.plotly_chart(CO2fig)

#===============相関2軸グラフ=======================
if uploaded_file1 and '相関2軸グラフ' in grafustock:
    #ヘッダー
    st.header("相関2軸グラフ")

    st.sidebar.write("""## 表示日付・温室選択""")
    select_dates = st.sidebar.date_input('表示日付の選択',value=(df_ex1.index[-1],df_ex1.index[-1]),min_value=df_ex1.index[0],max_value=df_ex1.index[-1])
    
    #温室番号選ぶ
    listnum = ['1','2','3','4','5','6','7','8','9']
    stocks = st.sidebar.selectbox(label="温室番号の選択",options = listnum)

    if '1' in stocks:
        chooseonsitu = df_ex1
    if '2' in stocks:
        chooseonsitu = df_ex2
    if '3' in stocks:
        chooseonsitu = df_ex3
    if '4' in stocks:
        chooseonsitu = df_ex4
    if '5' in stocks:
        chooseonsitu = df_ex5
    if '6' in stocks:
        chooseonsitu = df_ex6
    if '7' in stocks:
        chooseonsitu = df_ex7
    if '8' in stocks:
        chooseonsitu = df_ex8
    if '9' in stocks:
        chooseonsitu = df_ex9

    #温室ごとグラフデータ定義
    selectday = chooseonsitu[select_dates[0].strftime("%Y-%m-%d"):select_dates[-1].strftime("%Y-%m-%d")]
    ondochart = go.Scattergl(x=selectday['データ生成日時'],
                        y=selectday['温度'] ,
                        marker_color='orangered',
                        line_width=1,
                        yaxis='y1',
                        name='温度')
    situdochart = go.Scattergl(x=selectday['データ生成日時'],
                        y=selectday['相対湿度'] ,
                        marker_color='dodgerblue',
                        line_width=1,
                        yaxis='y1',
                        name='相対湿度')
    nisyachart = go.Scattergl(x=selectday['データ生成日時'],
                        y=selectday['日射'] ,
                        marker_color='darkorange',
                        line_width=1,
                        yaxis='y2',
                        name='日射',)
    CO2chart = go.Scattergl(x=selectday['データ生成日時'],
                        y=selectday['CO2濃度'] ,
                        marker_color='mediumseagreen',
                        line_width=1,
                        yaxis='y2',
                        name='CO2濃度')
    #レイアウト設定
    layout = go.Layout(title=dict(text='<b>【相関グラフ】'),xaxis = dict(title = '日付'), font=dict(size=15),
              yaxis1 = dict(side = 'left',range = [0, 110],showgrid=False),                            
              yaxis2 = dict(side = 'right', overlaying = 'y1', range = [0,1100],showgrid=False),
              legend=dict(xanchor='left',yanchor='bottom',x=0.32,y=1.0,orientation='h'),width=1350,height=700)
    #グラフ表示
    fig = dict(data = [ondochart, situdochart,nisyachart, CO2chart],layout=layout)
    st.plotly_chart(fig)

#===============近日比較グラフ=======================
if uploaded_file1 and '3.近日比較グラフ' in grafustock:
    #ヘッダー
    st.header("近日比較グラフ")
    #サイドバーの日付選ぶ
    st.sidebar.write("""## 表示日付・温室選択""")
    #指定日の指定
    # df_ex1.insert(1,"月日2",df_ex1["データ生成日時"].dt.strftime("%m月%d日"))
    MMdd_list = sorted(set(df_changereadfile['月日2'].to_list()),reverse=True)
    select_dates = st.sidebar.selectbox('表示日付の選択',MMdd_list)
    #指定日の前日
    if select_dates == MMdd_list[-1]:
        mode_no = 1
        secondselect_dates_index = MMdd_list.index(select_dates)
        thirdselect_dates_index = MMdd_list.index(select_dates)
        forth_dates_index = MMdd_list.index(select_dates)
        fifth_dates_index = MMdd_list.index(select_dates)
        sixth_dates_index = MMdd_list.index(select_dates)
        seventh_dates_index = MMdd_list.index(select_dates)
    elif select_dates == MMdd_list[-2]:
        mode_no = 2
        secondselect_dates_index = MMdd_list.index(select_dates) + 1
        thirdselect_dates_index = MMdd_list.index(select_dates)
        forth_dates_index = MMdd_list.index(select_dates)
        fifth_dates_index = MMdd_list.index(select_dates)
        sixth_dates_index = MMdd_list.index(select_dates)
        seventh_dates_index = MMdd_list.index(select_dates)
    elif select_dates == MMdd_list[-3]:
        mode_no = 3
        secondselect_dates_index = MMdd_list.index(select_dates) + 1
        thirdselect_dates_index = MMdd_list.index(select_dates) + 2
        forth_dates_index = MMdd_list.index(select_dates)
        fifth_dates_index = MMdd_list.index(select_dates)
        sixth_dates_index = MMdd_list.index(select_dates)
        seventh_dates_index = MMdd_list.index(select_dates)
    elif select_dates == MMdd_list[-4]:
        mode_no = 4
        secondselect_dates_index = MMdd_list.index(select_dates) + 1
        thirdselect_dates_index = MMdd_list.index(select_dates) + 2
        forth_dates_index = MMdd_list.index(select_dates) + 3
        fifth_dates_index = MMdd_list.index(select_dates)
        sixth_dates_index = MMdd_list.index(select_dates)
        seventh_dates_index = MMdd_list.index(select_dates)
    elif select_dates == MMdd_list[-5]:
        mode_no = 5
        secondselect_dates_index = MMdd_list.index(select_dates) + 1
        thirdselect_dates_index = MMdd_list.index(select_dates) + 2
        forth_dates_index = MMdd_list.index(select_dates) + 3
        fifth_dates_index = MMdd_list.index(select_dates) + 4
        sixth_dates_index = MMdd_list.index(select_dates)
        seventh_dates_index = MMdd_list.index(select_dates)
    elif select_dates == MMdd_list[-6]:
        mode_no = 6
        secondselect_dates_index = MMdd_list.index(select_dates) + 1
        thirdselect_dates_index = MMdd_list.index(select_dates) + 2
        forth_dates_index = MMdd_list.index(select_dates) + 3
        fifth_dates_index = MMdd_list.index(select_dates) + 4
        sixth_dates_index = MMdd_list.index(select_dates) + 5
        seventh_dates_index = MMdd_list.index(select_dates)
    else:
        mode_no = 7
        secondselect_dates_index = MMdd_list.index(select_dates) + 1
        thirdselect_dates_index = MMdd_list.index(select_dates) + 2
        forth_dates_index = MMdd_list.index(select_dates) + 3
        fifth_dates_index = MMdd_list.index(select_dates) + 4
        sixth_dates_index = MMdd_list.index(select_dates) + 5
        seventh_dates_index = MMdd_list.index(select_dates) + 6
    secondselect_dates = MMdd_list[secondselect_dates_index]
    thirdselect_dates = MMdd_list[thirdselect_dates_index]
    forth_dates = MMdd_list[forth_dates_index]
    fifth_dates = MMdd_list[fifth_dates_index]
    sixth_dates = MMdd_list[sixth_dates_index]
    seventh_dates = MMdd_list[seventh_dates_index]
    #温室番号選ぶ
    listnum = ['1','2','3','4','5','6','7','8','9']
    stocks = st.sidebar.selectbox(label="温室番号の選択",
                options = listnum)
    if '1' in stocks:
        selectday = df_ex1[df_ex1['月日2'] == select_dates]
        yesterday = df_ex1[df_ex1['月日2'] == secondselect_dates]
        third = df_ex1[df_ex1['月日2'] == thirdselect_dates]
        forth = df_ex1[df_ex1['月日2'] == forth_dates]
        fifth = df_ex1[df_ex1['月日2'] == fifth_dates]
        sixth = df_ex1[df_ex1['月日2'] == sixth_dates]
        seventh = df_ex1[df_ex1['月日2'] == seventh_dates]
    if '2' in stocks:
        selectday = df_ex2[df_ex2['月日2'] == select_dates]
        yesterday = df_ex2[df_ex2['月日2'] == secondselect_dates]
        third = df_ex2[df_ex2['月日2'] == thirdselect_dates]
        forth = df_ex2[df_ex2['月日2'] == forth_dates]
        fifth = df_ex2[df_ex2['月日2'] == fifth_dates]
        sixth = df_ex2[df_ex2['月日2'] == sixth_dates]
        seventh = df_ex2[df_ex2['月日2'] == seventh_dates]
    if '3' in stocks:
        selectday = df_ex3[df_ex3['月日2'] == select_dates]
        yesterday = df_ex3[df_ex3['月日2'] == secondselect_dates]
        third = df_ex3[df_ex3['月日2'] == thirdselect_dates]
        forth = df_ex3[df_ex3['月日2'] == forth_dates]
        fifth = df_ex3[df_ex3['月日2'] == fifth_dates]
        sixth = df_ex3[df_ex3['月日2'] == sixth_dates]
        seventh = df_ex3[df_ex3['月日2'] == seventh_dates]
    if '4' in stocks:
        selectday = df_ex4[df_ex4['月日2'] == select_dates]
        yesterday = df_ex4[df_ex4['月日2'] == secondselect_dates]
        third = df_ex4[df_ex4['月日2'] == thirdselect_dates]
        forth = df_ex4[df_ex4['月日2'] == forth_dates]
        fifth = df_ex4[df_ex4['月日2'] == fifth_dates]
        sixth = df_ex4[df_ex4['月日2'] == sixth_dates]
        seventh = df_ex4[df_ex4['月日2'] == seventh_dates]
    if '5' in stocks:
        selectday = df_ex5[df_ex5['月日2'] == select_dates]
        yesterday = df_ex5[df_ex5['月日2'] == secondselect_dates]
        third = df_ex5[df_ex5['月日2'] == thirdselect_dates]
        forth = df_ex5[df_ex5['月日2'] == forth_dates]
        fifth = df_ex5[df_ex5['月日2'] == fifth_dates]
        sixth = df_ex5[df_ex5['月日2'] == sixth_dates]
        seventh = df_ex5[df_ex5['月日2'] == seventh_dates]
    if '6' in stocks:
        selectday = df_ex6[df_ex6['月日2'] == select_dates]
        yesterday = df_ex6[df_ex6['月日2'] == secondselect_dates]
        third = df_ex6[df_ex6['月日2'] == thirdselect_dates]
        forth = df_ex6[df_ex6['月日2'] == forth_dates]
        fifth = df_ex6[df_ex6['月日2'] == fifth_dates]
        sixth = df_ex6[df_ex6['月日2'] == sixth_dates]
        seventh = df_ex6[df_ex6['月日2'] == seventh_dates]
    if '7' in stocks:
        selectday = df_ex7[df_ex7['月日2'] == select_dates]
        yesterday = df_ex7[df_ex7['月日2'] == secondselect_dates]
        third = df_ex7[df_ex7['月日2'] == thirdselect_dates]
        forth = df_ex7[df_ex7['月日2'] == forth_dates]
        fifth = df_ex7[df_ex7['月日2'] == fifth_dates]
        sixth = df_ex7[df_ex7['月日2'] == sixth_dates]
        seventh = df_ex7[df_ex7['月日2'] == seventh_dates]
    if '8' in stocks:
        selectday = df_ex8[df_ex8['月日2'] == select_dates]
        yesterday = df_ex8[df_ex8['月日2'] == secondselect_dates]
        third = df_ex8[df_ex8['月日2'] == thirdselect_dates]
        forth = df_ex8[df_ex8['月日2'] == forth_dates]
        fifth = df_ex8[df_ex8['月日2'] == fifth_dates]
        sixth = df_ex8[df_ex8['月日2'] == sixth_dates]
        seventh = df_ex8[df_ex8['月日2'] == seventh_dates]
    if '9' in stocks:
        selectday = df_ex9[df_ex9['月日2'] == select_dates]
        yesterday = df_ex9[df_ex9['月日2'] == secondselect_dates]
        third = df_ex9[df_ex9['月日2'] == thirdselect_dates]
        forth = df_ex9[df_ex9['月日2'] == forth_dates]
        fifth = df_ex9[df_ex9['月日2'] == fifth_dates]
        sixth = df_ex9[df_ex9['月日2'] == sixth_dates]
        seventh = df_ex9[df_ex9['月日2'] == seventh_dates]
    #レイアウト設定
    layout = go.Layout(title=dict(text='<b>【比較グラフ】'),xaxis = dict(title = '日付'), font=dict(size=15),
              yaxis1 = dict(side = 'left', showgrid=False,range = [0, 110]),                            
              legend=dict(xanchor='left',yanchor='bottom',x=0.32,y=1.0,orientation='h'))
    #温室ごとグラフデータ定義
    ondofig = go.Figure(layout=layout_Ondo)
    situdofig = go.Figure(layout=layout_Situdo)
    nisyafig = go.Figure(layout=layout_Nisya)
    CO2fig = go.Figure(layout=layout_Co2)
    def ondo_0():
        ondofig.add_traces(go.Scattergl(x=selectday["時間"],
                                y= selectday['温度'] ,
                                marker_color='mediumseagreen',
                                line_width=1,
                                yaxis='y1',
                                name=select_dates))
    def ondo_1():
        ondofig.add_traces(go.Scattergl(x=yesterday["時間"],
                                y=yesterday['温度'] ,
                                marker_color='orangered',
                                line_width=1,
                                yaxis='y1',
                                name=secondselect_dates))
    def ondo_2():
        ondofig.add_traces(go.Scattergl(x=third["時間"],
                                y= third['温度'] ,
                                marker_color='hotpink',
                                line_width=1,
                                yaxis='y1',
                                name=thirdselect_dates))
    def ondo_3():
        ondofig.add_traces(go.Scattergl(x=forth["時間"],
                                y= forth['温度'] ,
                                marker_color='dodgerblue',
                                line_width=1,
                                yaxis='y1',
                                name=forth_dates))
    def ondo_4():
        ondofig.add_traces(go.Scattergl(x=fifth["時間"],
                                y= fifth['温度'] ,
                                marker_color='darkorange',
                                line_width=1,
                                yaxis='y1',
                                name=fifth_dates))
    def ondo_5():
        ondofig.add_traces(go.Scattergl(x=sixth["時間"],
                                y= sixth['温度'] ,
                                marker_color='mediumpurple',
                                line_width=1,
                                yaxis='y1',
                                name=sixth_dates))
    def ondo_6():
        ondofig.add_traces(go.Scattergl(x=seventh["時間"],
                                y= seventh['温度'] ,
                                marker_color='tan',
                                line_width=1,
                                yaxis='y1',
                                name=seventh_dates))    
    def nisya_0():
        nisyafig.add_traces(go.Scattergl(x=selectday["時間"],
                                y= selectday['日射'] ,
                                marker_color='mediumseagreen',
                                line_width=1,
                                yaxis='y1',
                                name=select_dates))
    def nisya_1():
        nisyafig.add_traces(go.Scattergl(x=yesterday["時間"],
                                y=yesterday['日射'] ,
                                marker_color='orangered',
                                line_width=1,
                                yaxis='y1',
                                name=secondselect_dates))
    def nisya_2():
        nisyafig.add_traces(go.Scattergl(x=third["時間"],
                                y= third['日射'] ,
                                marker_color='hotpink',
                                line_width=1,
                                yaxis='y1',
                                name=thirdselect_dates))
    def nisya_3():
        nisyafig.add_traces(go.Scattergl(x=forth["時間"],
                                y= forth['日射'] ,
                                marker_color='dodgerblue',
                                line_width=1,
                                yaxis='y1',
                                name=forth_dates))
    def nisya_4():
        nisyafig.add_traces(go.Scattergl(x=fifth["時間"],
                                y= fifth['日射'] ,
                                marker_color='darkorange',
                                line_width=1,
                                yaxis='y1',
                                name=fifth_dates))
    def nisya_5():
        nisyafig.add_traces(go.Scattergl(x=sixth["時間"],
                                y= sixth['日射'] ,
                                marker_color='mediumpurple',
                                line_width=1,
                                yaxis='y1',
                                name=sixth_dates))
    def nisya_6():
        nisyafig.add_traces(go.Scattergl(x=seventh["時間"],
                                y= seventh['日射'] ,
                                marker_color='tan',
                                line_width=1,
                                yaxis='y1',
                                name=seventh_dates))                                
    def situdo_0():
        situdofig.add_traces(go.Scattergl(x=selectday["時間"],
                                y= selectday['相対湿度'] ,
                                marker_color='mediumseagreen',
                                line_width=1,
                                yaxis='y1',
                                name=select_dates))
    def situdo_1():
        situdofig.add_traces(go.Scattergl(x=yesterday["時間"],
                                y=yesterday['相対湿度'] ,
                                marker_color='orangered',
                                line_width=1,
                                yaxis='y1',
                                name=secondselect_dates))
    def situdo_2():
        situdofig.add_traces(go.Scattergl(x=third["時間"],
                                y= third['相対湿度'] ,
                                marker_color='hotpink',
                                line_width=1,
                                yaxis='y1',
                                name=thirdselect_dates))
    def situdo_3():
        situdofig.add_traces(go.Scattergl(x=forth["時間"],
                                y= forth['相対湿度'] ,
                                marker_color='dodgerblue',
                                line_width=1,
                                yaxis='y1',
                                name=forth_dates))
    def situdo_4():
        situdofig.add_traces(go.Scattergl(x=fifth["時間"],
                                y= fifth['相対湿度'] ,
                                marker_color='darkorange',
                                line_width=1,
                                yaxis='y1',
                                name=fifth_dates))
    def situdo_5():
        situdofig.add_traces(go.Scattergl(x=sixth["時間"],
                                y= sixth['相対湿度'] ,
                                marker_color='mediumpurple',
                                line_width=1,
                                yaxis='y1',
                                name=sixth_dates))
    def situdo_6():
        situdofig.add_traces(go.Scattergl(x=seventh["時間"],
                                y= seventh['相対湿度'] ,
                                marker_color='tan',
                                line_width=1,
                                yaxis='y1',
                                name=seventh_dates))                                
    def CO2_0():
        CO2fig.add_traces(go.Scattergl(x=selectday["時間"],
                                y= selectday['CO2濃度'] ,
                                marker_color='mediumseagreen',
                                line_width=1,
                                yaxis='y1',
                                name=select_dates))
    def CO2_1():
        CO2fig.add_traces(go.Scattergl(x=yesterday["時間"],
                                y=yesterday['CO2濃度'] ,
                                marker_color='orangered',
                                line_width=1,
                                yaxis='y1',
                                name=secondselect_dates))
    def CO2_2():
        CO2fig.add_traces(go.Scattergl(x=third["時間"],
                                y= third['CO2濃度'] ,
                                marker_color='hotpink',
                                line_width=1,
                                yaxis='y1',
                                name=thirdselect_dates))
    def CO2_3():
        CO2fig.add_traces(go.Scattergl(x=forth["時間"],
                                y= forth['CO2濃度'] ,
                                marker_color='dodgerblue',
                                line_width=1,
                                yaxis='y1',
                                name=forth_dates))
    def CO2_4():
        CO2fig.add_traces(go.Scattergl(x=fifth["時間"],
                                y= fifth['CO2濃度'] ,
                                marker_color='darkorange',
                                line_width=1,
                                yaxis='y1',
                                name=fifth_dates))
    def CO2_5():
        CO2fig.add_traces(go.Scattergl(x=sixth["時間"],
                                y= sixth['CO2濃度'] ,
                                marker_color='mediumpurple',
                                line_width=1,
                                yaxis='y1',
                                name=sixth_dates))
    def CO2_6():
        CO2fig.add_traces(go.Scattergl(x=seventh["時間"],
                                y= seventh['CO2濃度'] ,
                                marker_color='tan',
                                line_width=1,
                                yaxis='y1',
                                name=seventh_dates))
    if mode_no == 1:
        ondo_0()
        nisya_0()
        situdo_0()
        CO2_0()
    elif mode_no == 2:
        ondo_0()
        nisya_0()
        situdo_0()
        CO2_0()
        ondo_1()
        nisya_1()
        situdo_1()
        CO2_1()
    elif mode_no == 3:
        ondo_0()
        nisya_0()
        situdo_0()
        CO2_0()
        ondo_1()
        nisya_1()
        situdo_1()
        CO2_1()
        ondo_2()
        nisya_2()
        situdo_2()
        CO2_2()
    elif mode_no == 4:
        ondo_0()
        nisya_0()
        situdo_0()
        CO2_0()
        ondo_1()
        nisya_1()
        situdo_1()
        CO2_1()
        ondo_2()
        nisya_2()
        situdo_2()
        CO2_2()
        ondo_3()
        nisya_3()
        situdo_3()
        CO2_3()
    elif mode_no == 5:
        ondo_0()
        nisya_0()
        situdo_0()
        CO2_0()
        ondo_1()
        nisya_1()
        situdo_1()
        CO2_1()
        ondo_2()
        nisya_2()
        situdo_2()
        CO2_2()
        ondo_3()
        nisya_3()
        situdo_3()
        CO2_3()
        ondo_4()
        nisya_4()
        situdo_4()
        CO2_4()
    elif mode_no == 6:
        ondo_0()
        nisya_0()
        situdo_0()
        CO2_0()
        ondo_1()
        nisya_1()
        situdo_1()
        CO2_1()
        ondo_2()
        nisya_2()
        situdo_2()
        CO2_2()
        ondo_3()
        nisya_3()
        situdo_3()
        CO2_3()
        ondo_4()
        nisya_4()
        situdo_4()
        CO2_4()
        ondo_5()
        nisya_5()
        situdo_5()
        CO2_5()
    else:
        ondo_0()
        nisya_0()
        situdo_0()
        CO2_0()
        ondo_1()
        nisya_1()
        situdo_1()
        CO2_1()
        ondo_2()
        nisya_2()
        situdo_2()
        CO2_2()
        ondo_3()
        nisya_3()
        situdo_3()
        CO2_3()
        ondo_4()
        nisya_4()
        situdo_4()
        CO2_4()
        ondo_5()
        nisya_5()
        situdo_5()
        CO2_5()
        ondo_6()
        nisya_6()
        situdo_6()
        CO2_6()
    #温度グラフ表示
    st.plotly_chart(ondofig)
    #日射グラフ表示
    st.plotly_chart(nisyafig)
    #相対湿度グラフ表示
    st.plotly_chart(situdofig)
    #CO2濃度グラフ表示
    st.plotly_chart(CO2fig)

#===============3ファイル比較グラフ=======================
if uploaded_file1 and uploaded_file2 and uploaded_file3 and '4.複数ファイルグラフ' in grafustock:
    #ヘッダー
    st.header("3ファイルグラフ")
    #サイドバーの温室番号選ぶ
    listnum = ['1','2','3','4','5','6','7','8','9']
    stocks = st.sidebar.selectbox(label="温室番号の選択",
                options = listnum)
    select_onsitu = int(stocks[0])
    if st.sidebar.checkbox("ファイル①の月日を選択する"):
        select_dates = st.sidebar.date_input('①表示日付の選択',value=(df_readfile1.index[0],df_readfile1.index[-1]),min_value=df_readfile1.index[0],max_value=df_readfile1.index[-1])
        df_readfile1 = df_readfile1[select_dates[0].strftime("%Y-%m-%d"):select_dates[-1].strftime("%Y-%m-%d")]
    if st.sidebar.checkbox("ファイル②の月日を選択する"):
        select_dates2 = st.sidebar.date_input('②表示日付の選択',value=(df_readfile2.index[0],df_readfile2.index[-1]),min_value=df_readfile2.index[0],max_value=df_readfile2.index[-1])
        df_readfile2 = df_readfile2[select_dates2[0].strftime("%Y-%m-%d"):select_dates2[-1].strftime("%Y-%m-%d")]
    if st.sidebar.checkbox("ファイル③の月日を選択する"):
        select_dates3 = st.sidebar.date_input('③表示日付の選択',value=(df_readfile3.index[0],df_readfile3.index[-1]),min_value=df_readfile3.index[0],max_value=df_readfile3.index[-1])
        df_readfile3 = df_readfile3[select_dates3[0].strftime("%Y-%m-%d"):select_dates3[-1].strftime("%Y-%m-%d")]

    #温室の識別
    def ex0():
        return df_readfile1[df_readfile1["温室"] == select_onsitu]
    def ex1():
        return df_readfile2[df_readfile2["温室"] == select_onsitu]
    def ex2():
        return df_readfile3[df_readfile3["温室"] == select_onsitu]
    df_ex0 = ex0()
    df_ex1 = ex1()
    df_ex2 = ex2()

    #ヘッダー
    st.header("温度・相対湿度・日射・CO2濃度のグラフ")

    #温室ごとグラフデータ定義
    ondofig = go.Figure(layout=layout_Ondo)
    situdofig = go.Figure(layout=layout_Situdo)
    nisyafig = go.Figure(layout=layout_Nisya)
    CO2fig = go.Figure(layout=layout_Co2)

    def hikaku1():
        ondofig.add_traces(go.Scattergl(x=df_ex0["月日時間"],
                                y=df_ex0['温度'] ,
                                marker_color='dodgerblue',
                                line_width=1,
                                name='ファイル1',))
        situdofig.add_traces(go.Scattergl(x=df_ex0["月日時間"],
                                y=df_ex0['相対湿度'] ,
                                marker_color='dodgerblue',
                                line_width=1,
                                name='ファイル1'
                                ))
        nisyafig.add_traces(go.Scattergl(x=df_ex0["月日時間"],
                                y=df_ex0['日射'] ,
                                marker_color='dodgerblue',
                                line_width=1,
                                name='ファイル1'))
        CO2fig.add_traces(go.Scattergl(x=df_ex0["月日時間"],
                                y=df_ex0['CO2濃度'] ,
                                marker_color='dodgerblue',
                                line_width=1,
                                name='ファイル1'))

        ondofig.add_traces(go.Scattergl(x=df_ex1["月日時間"],
                                y=df_ex1['温度'] ,
                                marker_color='orangered',
                                line_width=1,
                                name='ファイル2',))
        situdofig.add_traces(go.Scattergl(x=df_ex1["月日時間"],
                                y=df_ex1['相対湿度'] ,
                                marker_color='orangered',
                                line_width=1,
                                name='ファイル2'
                                ))
        nisyafig.add_traces(go.Scattergl(x=df_ex1["月日時間"],
                                y=df_ex1['日射'] ,
                                marker_color='orangered',
                                line_width=1,
                                name='ファイル2'))
        CO2fig.add_traces(go.Scattergl(x=df_ex1["月日時間"],
                                y=df_ex1['CO2濃度'] ,
                                marker_color='orangered',
                                line_width=1,
                                name='ファイル2'))

        ondofig.add_traces(go.Scattergl(x=df_ex2["月日時間"],
                                y=df_ex2['温度'] ,
                                marker_color='mediumseagreen',
                                line_width=1,
                                name='ファイル3'))
        situdofig.add_traces(go.Scattergl(x=df_ex2["月日時間"],
                                y=df_ex2['相対湿度'] ,
                                marker_color='mediumseagreen',
                                line_width=1,
                                name='ファイル3'))
        nisyafig.add_traces(go.Scattergl(x=df_ex2["月日時間"],
                                y=df_ex2['日射'] ,
                                marker_color='mediumseagreen',
                                line_width=1,
                                name='ファイル3'))
        CO2fig.add_traces(go.Scattergl(x=df_ex2["月日時間"],
                                y=df_ex2['CO2濃度'] ,
                                marker_color='mediumseagreen',
                                line_width=1,
                                name='ファイル3'))
    hikaku1()

    #温度グラフ表示
    st.plotly_chart(ondofig)
    #日射グラフ表示
    st.plotly_chart(nisyafig)
    #相対湿度グラフ表示
    st.plotly_chart(situdofig)
    #CO2濃度グラフ表示
    st.plotly_chart(CO2fig)

#===============2ファイル比較グラフ=======================
if uploaded_file1 and uploaded_file2 and not uploaded_file3 and '複数ファイルグラフ' in grafustock:
    #ヘッダー
    st.header("2ファイル比較グラフ")
    #サイドバーの温室番号選ぶ
    listnum = ['1','2','3','4','5','6','7','8','9']
    stocks = st.sidebar.selectbox(label="温室番号の選択",
                options = listnum,key=4)
    select_onsitu = int(stocks[0])
    # def ex1():
    #     return df_readfile1[df_readfile1["温室"] == select_onsitu]
    # def ex2():
    #     return df_readfile2[df_readfile2["温室"] == select_onsitu]
    # if st.checkbox("メインファイル変更"):
    #         df_ex2 = ex1()
    #         df_ex1 = ex2()
    # else:
    #         df_ex1 = ex1()
    #         df_ex2 = ex2()
    if st.sidebar.checkbox("ファイル①の月日を選択する"):
        select_dates = st.sidebar.date_input('①表示日付の選択',value=(df_readfile1.index[0],df_readfile1.index[-1]),min_value=df_readfile1.index[0],max_value=df_readfile1.index[-1])
        df_readfile1 = df_readfile1[select_dates[0].strftime("%Y-%m-%d"):select_dates[-1].strftime("%Y-%m-%d")]
    if st.sidebar.checkbox("ファイル②の月日を選択する"):
        select_dates2 = st.sidebar.date_input('②表示日付の選択',value=(df_readfile2.index[0],df_readfile2.index[-1]),min_value=df_readfile2.index[0],max_value=df_readfile2.index[-1])
        df_readfile2 = df_readfile2[select_dates2[0].strftime("%Y-%m-%d"):select_dates2[-1].strftime("%Y-%m-%d")]

    def ex1():
        return df_readfile1[df_readfile1["温室"] == select_onsitu]
    def ex2():
        return df_readfile2[df_readfile2["温室"] == select_onsitu]
    if st.checkbox("メインファイル変更"):
            df_ex2 = ex1()
            df_ex1 = ex2()
    else:
            df_ex1 = ex1()
            df_ex2 = ex2()

    #温室ごとグラフデータ定義
    ondofig = go.Figure(layout=layout_Ondo)
    situdofig = go.Figure(layout=layout_Situdo)
    nisyafig = go.Figure(layout=layout_Nisya)
    CO2fig = go.Figure(layout=layout_Co2)

    def hikaku2():
        ondofig.add_traces(go.Scattergl(x=df_ex1["月日時間"],
                                y= df_ex1['温度'] ,
                                marker_color='dodgerblue',
                                line_width=1,
                                yaxis='y1',
                                name='ファイル1'))
        situdofig.add_traces(go.Scattergl(x=df_ex1["月日時間"],
                                y=df_ex1['相対湿度'] ,
                                marker_color='dodgerblue',
                                line_width=1,
                                name='ファイル1',
                                yaxis='y1'))
        nisyafig.add_traces(go.Scattergl(x=df_ex1["月日時間"],
                                y=df_ex1['日射'] ,
                                marker_color='dodgerblue',
                                line_width=1,
                                name='ファイル1',
                                yaxis='y1'))
        CO2fig.add_traces(go.Scattergl(x=df_ex1["月日時間"],
                                y=df_ex1['CO2濃度'] ,
                                marker_color='dodgerblue',
                                line_width=1,
                                name='ファイル1',
                                yaxis='y1'))

        ondofig.add_traces(go.Scattergl(x=df_ex2["月日時間"],
                                y=df_ex2['温度'] ,
                                marker_color='orangered',
                                line_width=1,
                                name='ファイル2',
                                yaxis='y1'))
        situdofig.add_traces(go.Scattergl(x=df_ex2["月日時間"],
                                y=df_ex2['相対湿度'] ,
                                marker_color='orangered',
                                line_width=1,
                                name='ファイル2',
                                yaxis='y1'))
        nisyafig.add_traces(go.Scattergl(x=df_ex2["月日時間"],
                                y=df_ex2['日射'] ,
                                marker_color='orangered',
                                line_width=1,
                                name='ファイル2',
                                yaxis='y1'))
        CO2fig.add_traces(go.Scattergl(x=df_ex2["月日時間"],
                                y=df_ex2['CO2濃度'] ,
                                marker_color='orangered',
                                line_width=1,
                                name='ファイル2',
                                yaxis='y1'))
    hikaku2()

    #温度グラフ表示
    st.plotly_chart(ondofig)
    #日射グラフ表示
    st.plotly_chart(nisyafig)
    #相対湿度グラフ表示
    st.plotly_chart(situdofig)
    #CO2濃度グラフ表示
    st.plotly_chart(CO2fig)

#================エラー回避=====================
if not uploaded_file1 and not uploaded_file2 and not uploaded_file3 and '複数ファイルグラフ' in grafustock:
    st.warning("複数ファイルをアップロードしてください")
if uploaded_file1 and not uploaded_file2 and not uploaded_file3 and '複数ファイルグラフ' in grafustock:
    st.warning("複数ファイルをアップロードしてください")