"""
Conversor PDF -> Markdown -> Lucas Ludwig
"""
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path

from docling.document_converter import DocumentConverter

class ConversorPDF:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("PDF -> Markdown")
        self.root.geometry("400x250")
        self.root.resizable(False, False)
        
        self.arquivo_selecionado = ""
        self.configurar_interface()
    
    def configurar_interface(self):
        # Título
        titulo = tk.Label(self.root, text="📄 Conversor PDF -> Markdown", 
                        font=("Impact", 16))
        titulo.pack(pady=15)
        
        # Botão selecionar arquivo
        botao_selecionar = tk.Button(self.root, text="📁 Selecionar PDF", 
                              command=self.selecionar_arquivo,
                              font=("Impact", 12),
                              bg="#3498db", fg="white",
                              width=20, height=1)
        botao_selecionar.pack(pady=8)
        
        # Label do arquivo selecionado
        self.label_arquivo = tk.Label(self.root, text="Nenhum arquivo selecionado",
                                  fg="gray", wraplength=350)
        self.label_arquivo.pack(pady=8)
        
        # Botão converter
        self.botao_converter = tk.Button(self.root, text="🚀 Converter", 
                                    command=self.converter_arquivo,
                                    font=("Impact", 12),
                                    bg="#60ffa2", fg="white",
                                    width=20, height=1,
                                    state="disabled")
        self.botao_converter.pack(pady=15)
    
    def selecionar_arquivo(self):
        file_path = filedialog.askopenfilename(
            title="Selecionar PDF",
            filetypes=[("PDF files", "*.pdf")]
        )
        
        if file_path:
            self.arquivo_selecionado = file_path
            filename = os.path.basename(file_path)
            self.label_arquivo.config(text=f"📄 {filename}", fg="black")
            self.botao_converter.config(state="normal")
    
    def converter_arquivo(self):
        if not self.arquivo_selecionado:
            return
        
        try:
            # Desabilitar botão durante conversão
            self.botao_converter.config(state="disabled", text="⏳ Convertendo...")
            self.root.update()
            
            # Converter
            conversor = DocumentConverter()
            resultado = conversor.convert(self.arquivo_selecionado)
            markdown = resultado.document.export_to_markdown()
            
            # Salvar
            output_file = Path(self.arquivo_selecionado).stem + ".md"
            output_path = os.path.join(os.path.dirname(self.arquivo_selecionado), output_file)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(markdown)
            
            # Sucesso
            messagebox.showinfo("Sucesso!", 
                               f"Convertido para:\n{output_file}")
            
            # Reabilitar botão
            self.botao_converter.config(state="normal", text="🚀 Converter")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro na conversão:\n{str(e)}")
            self.botao_converter.config(state="normal", text="🚀 Converter")
    
    def executar(self):
        self.root.mainloop()

def main():
    app = ConversorPDF()
    app.executar()

if __name__ == "__main__":
    main()