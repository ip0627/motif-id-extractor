# motif-id-extractor
TSV file motif ID extraction tool with GUI
Motif ID Extractor
TSVファイルからmotif_alt_idを解析し、特定の条件に合致するMotif IDを抽出するGUIツールです。
機能

TSVファイルからmotif_alt_idとsequence_nameを読み取り
Raxcis_B_floridae以外の6種類すべてで存在するMotif IDを抽出
結果をTSV形式で保存
直感的なGUIインターフェース

対象となるsequence_name

Raxcis_P_marinus
Raxcis_M_musculus
Raxcis_X_tropicalis
Raxcis_G_gallus
Raxcis_L_oculatus
Raxcis_H_sapiens

抽出条件

Raxcis_B_floridaeが含まれていない
上記6種類すべてが含まれている

必要な環境

Python 3.6以上
tkinter（通常Pythonに標準で含まれています）

使用方法

スクリプトを実行してGUIを起動

bashpython motif_extractor.py

「TSVファイルを選択」ボタンで入力ファイルを選択
「処理実行」ボタンで処理開始
結果確認後、TSVファイルとして保存

入力ファイル形式

TSVファイル（タブ区切り）
1行目にヘッダー行が必要
2列目: motif_alt_id（例：MA0600.1.RFX2）
3列目: sequence_name（例：Raxcis_M_musculus）

出力ファイル形式
tsvMotif_ID	Sequence_Names
CREM	Raxcis_G_gallus, Raxcis_H_sapiens, Raxcis_L_oculatus, Raxcis_M_musculus, Raxcis_P_marinus, Raxcis_X_tropicalis
NFKB1	Raxcis_G_gallus, Raxcis_H_sapiens, Raxcis_L_oculatus, Raxcis_M_musculus, Raxcis_P_marinus, Raxc
