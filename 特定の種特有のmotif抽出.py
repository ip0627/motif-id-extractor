import tkinter as tk
from tkinter import filedialog, messagebox
import csv
import os
from collections import defaultdict

class MotifExtractor:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Motif ID Extractor")
        self.root.geometry("600x400")
        
        # 対象のsequence_name（Raxcis_B_floridae以外の6種類）
        self.target_sequences = {
            "Raxcis_P_marinus",
            "Raxcis_M_musculus", 
            "Raxcis_X_tropicalis",
            "Raxcis_G_gallus",
            "Raxcis_L_oculatus",
            "Raxcis_H_sapiens"
        }
        
        self.setup_ui()
    
    def setup_ui(self):
        """UIの設定"""
        # メインフレーム
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # タイトル
        title_label = tk.Label(main_frame, text="Motif ID Extractor", 
                              font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # 説明
        desc_text = """
このツールは以下の処理を行います：
1. TSVファイルからmotif_alt_idとsequence_nameを読み取り
2. Raxcis_B_floridae以外の6種類すべてで存在するMotif IDを抽出
3. 結果をTSV形式で保存
        """
        desc_label = tk.Label(main_frame, text=desc_text, justify=tk.LEFT)
        desc_label.pack(pady=(0, 20))
        
        # ファイル選択ボタン
        file_button = tk.Button(main_frame, text="TSVファイルを選択", 
                               command=self.select_file, font=("Arial", 12))
        file_button.pack(pady=10)
        
        # 選択されたファイル名表示
        self.file_label = tk.Label(main_frame, text="ファイルが選択されていません", 
                                  fg="gray")
        self.file_label.pack(pady=5)
        
        # 実行ボタン
        self.process_button = tk.Button(main_frame, text="処理実行", 
                                       command=self.process_file, 
                                       font=("Arial", 12), state=tk.DISABLED)
        self.process_button.pack(pady=20)
        
        # 結果表示エリア
        result_frame = tk.Frame(main_frame)
        result_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(result_frame, text="処理結果:", font=("Arial", 10, "bold")).pack(anchor=tk.W)
        
        # スクロール可能なテキストエリア
        text_frame = tk.Frame(result_frame)
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        self.result_text = tk.Text(text_frame, height=10, wrap=tk.WORD)
        scrollbar = tk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.result_text.yview)
        self.result_text.configure(yscrollcommand=scrollbar.set)
        
        self.result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.selected_file = None
    
    def select_file(self):
        """ファイル選択ダイアログ"""
        file_path = filedialog.askopenfilename(
            title="TSVファイルを選択",
            filetypes=[("TSV files", "*.tsv"), ("All files", "*.*")]
        )
        
        if file_path:
            self.selected_file = file_path
            self.file_label.config(text=f"選択されたファイル: {os.path.basename(file_path)}", 
                                  fg="blue")
            self.process_button.config(state=tk.NORMAL)
    
    def extract_motif_id(self, motif_alt_id):
        """motif_alt_idから3番目のパート（ID）を抽出"""
        parts = motif_alt_id.split('.')
        if len(parts) >= 3:
            return parts[2]
        return None
    
    def process_file(self):
        """ファイル処理メイン"""
        if not self.selected_file:
            messagebox.showerror("エラー", "ファイルが選択されていません")
            return
        
        try:
            # IDごとにsequence_nameを記録
            id_to_sequences = defaultdict(set)
            
            with open(self.selected_file, 'r', encoding='utf-8') as f:
                reader = csv.reader(f, delimiter='\t')
                
                # ヘッダー行をスキップ
                next(reader)
                
                for row in reader:
                    if len(row) < 3:
                        continue
                    
                    motif_alt_id = row[1]  # 2列目（0-indexed）
                    sequence_name = row[2]  # 3列目（0-indexed）
                    
                    # motif_alt_idからIDを抽出
                    motif_id = self.extract_motif_id(motif_alt_id)
                    if motif_id is None:
                        continue
                    
                    # IDとsequence_nameの関係を記録
                    id_to_sequences[motif_id].add(sequence_name)
            
            # 条件に合致するIDを抽出
            matching_ids = []
            
            for motif_id, sequences in id_to_sequences.items():
                # Raxcis_B_floridaeが含まれていないかチェック
                if "Raxcis_B_floridae" not in sequences:
                    # 他の6種類すべてが含まれているかチェック
                    sequences_for_id = sequences & self.target_sequences
                    if sequences_for_id == self.target_sequences:  # 6種類すべてが含まれている
                        matching_ids.append((motif_id, sequences_for_id))
            
            # 結果を保存
            if matching_ids:
                self.save_results(matching_ids)
                self.display_results(matching_ids)
            else:
                self.result_text.delete(1.0, tk.END)
                self.result_text.insert(tk.END, "条件に合致するMotif IDは見つかりませんでした")
                messagebox.showinfo("結果", "条件に合致するMotif IDは見つかりませんでした")
        
        except Exception as e:
            messagebox.showerror("エラー", f"ファイル処理中にエラーが発生しました: {str(e)}")
    
    def save_results(self, matching_ids):
        """結果をTSVファイルに保存"""
        output_file = filedialog.asksaveasfilename(
            title="結果を保存",
            defaultextension=".tsv",
            filetypes=[("TSV files", "*.tsv"), ("All files", "*.*")]
        )
        
        if output_file:
            try:
                with open(output_file, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f, delimiter='\t')
                    
                    # ヘッダー行
                    writer.writerow(["Motif_ID", "Sequence_Names"])
                    
                    # データ行
                    for motif_id, sequences in sorted(matching_ids):
                        sequence_list = ', '.join(sorted(sequences))
                        writer.writerow([motif_id, sequence_list])
                
                messagebox.showinfo("保存完了", f"結果が保存されました: {os.path.basename(output_file)}")
            
            except Exception as e:
                messagebox.showerror("保存エラー", f"ファイル保存中にエラーが発生しました: {str(e)}")
    
    def display_results(self, matching_ids):
        """結果をGUIに表示"""
        self.result_text.delete(1.0, tk.END)
        
        result_text = f"条件に合致するMotif ID: {len(matching_ids)}個\n\n"
        
        for motif_id, sequences in sorted(matching_ids):
            sequence_list = ', '.join(sorted(sequences))
            result_text += f"{motif_id}\t{sequence_list}\n"
        
        self.result_text.insert(tk.END, result_text)
    
    def run(self):
        """アプリケーション実行"""
        self.root.mainloop()

def main():
    app = MotifExtractor()
    app.run()

if __name__ == "__main__":
    main()