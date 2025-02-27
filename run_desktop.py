import sys
import os

if __name__ == "__main__":
    # 设置项目根目录
    project_root = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, project_root)
    
    from src.desktop.gui_app import DoctorGUI
    app = DoctorGUI()
    app.root.mainloop() 