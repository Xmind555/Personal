import os
import PyPDF2

def encrypt_pdf(input_pdf_path, password):
    """加密PDF文件"""
    with open(input_pdf_path, 'rb') as input_file:
        reader = PyPDF2.PdfReader(input_file)
        writer = PyPDF2.PdfWriter()

        for page in reader.pages:
            writer.add_page(page)

        writer.encrypt(password)

        dir_name = os.path.dirname(input_pdf_path)
        base_name = os.path.basename(input_pdf_path)
        output_pdf_name = f"{os.path.splitext(base_name)[0]}-enc.pdf"
        output_pdf_path = os.path.join(dir_name, output_pdf_name)

        with open(output_pdf_path, 'wb') as output_file:
            writer.write(output_file)

    return output_pdf_path

def decrypt_pdf(input_pdf_path, password):
    """解密PDF文件"""
    with open(input_pdf_path, 'rb') as input_file:
        reader = PyPDF2.PdfReader(input_file)

        if not reader.decrypt(password):
            raise ValueError("密码错误，无法解密PDF文件。")

        writer = PyPDF2.PdfWriter()

        for page in reader.pages:
            writer.add_page(page)

        dir_name = os.path.dirname(input_pdf_path)
        base_name = os.path.basename(input_pdf_path)
        output_pdf_name = f"{os.path.splitext(base_name)[0]}-dec.pdf"
        output_pdf_path = os.path.join(dir_name, output_pdf_name)

        with open(output_pdf_path, 'wb') as output_file:
            writer.write(output_file)

    return output_pdf_path

def main():
    while True:
        print("\nPDF工具菜单：")
        print("1. PDF加密")
        print("2. PDF解密")
        print("3. 退出")

        choice = input("请选择功能 (1/2/3): ").strip()

        if choice == "1":
            input_pdf_path = input("请输入PDF文件路径: ").strip('"')
            password = input("请输入加密密码: ")
            try:
                output_path = encrypt_pdf(input_pdf_path, password)
                print(f"加密完成，生成的文件路径为: {output_path}")
            except Exception as e:
                print(f"加密失败: {e}")

        elif choice == "2":
            input_pdf_path = input("请输入PDF文件路径: ").strip('"')
            password = input("请输入解密密码: ")
            try:
                output_path = decrypt_pdf(input_pdf_path, password)
                print(f"解密完成，生成的文件路径为: {output_path}")
            except Exception as e:
                print(f"解密失败: {e}")

        elif choice == "3":
            print("退出程序。再见！")
            break

        else:
            print("无效的选项，请重新选择。")

if __name__ == "__main__":
    main()
