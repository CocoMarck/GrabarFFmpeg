import Modulo_Util as Util
import os

import gi
import Modulo_FFmpeg as FFmpeg

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


sys = Util.System()

class Dialog_Start(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title='Dialogo Empezar', transient_for=parent, flags=0)
        self.set_default_size(256, 64)
                
        box_v = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        
        label_title = Gtk.Label()
        label_title.set_markup('<b>Dialogo Empezar</b>')
        label_title.set_justify(Gtk.Justification.CENTER)
        box_v.pack_start(label_title, True, True, 0)
        
        btn_demo = Gtk.Button(label='Boton de prueba')
        btn_demo.connect('clicked', self.evt_demo)
        box_v.pack_start(btn_demo, True, True, 0)
        
        box_main = self.get_content_area()
        box_main.add(box_v)
        self.show_all()
        
    def evt_demo(self, widget):
        print('Boton de prueba, precionado')


class Command_Run(Gtk.Dialog):
    def __init__(self, parent, cfg='', txt='Ejecutar Comando'):
        super().__init__(title='Ejecutar comando', transient_for=parent, flags=0)
        self.set_default_size(256, 0)
        self.cfg = cfg
        
        box_v = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        
        label = Gtk.Label()
        label.set_markup(f'<b>Comando</b>')
        #label.set_justify(Gtk.Justification.CENTER)
        label.set_line_wrap(True)
        box_v.pack_start(label, True, True, 0)
        
        label = Gtk.Label()
        label.set_markup(f'<i>{self.cfg}</i>')
        #label.set_justify(Gtk.Justification.LEFT)
        label.set_line_wrap(True)
        label.set_selectable(True)
        box_v.pack_start(label, True, True, 0)
        
        button = Gtk.Button(label=txt)
        button.connect('clicked', self.evt_command_run)
        box_v.pack_start(button, True, True, 0)
        
        box_main = self.get_content_area()
        box_main.add(box_v)
        self.show_all()
        
    def evt_command_run(self, widget):
        os.system(f"xfce4-terminal --startup-id= -e '{self.cfg}'")
        self.destroy()


class Dialog_FFmpegVideo(Gtk.Dialog):
    def __init__(self, parent, opc='CompressVideos'):
        self.cfg = ''
        self.opc = opc
    
        if self.opc == 'VideoCompress': self.txt_title = 'Comprimir Video'
        elif self.opc == 'VideoRecord': self.txt_title = 'Grabar Video'
        else: 'Title for else'
    
        super().__init__(title=f'{opc}', transient_for=parent, flags=0)
        self.set_default_size(352, 0)
        
        box_data = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=16)
        
        label_title = Gtk.Label()
        label_title.set_markup(f'<big><b>{self.txt_title}</b></big>\n')
        box_data.pack_start(label_title, True, True, 8)
        
        if self.opc == 'VideoCompress':
            btn_path = Gtk.Button(label='Elegir Video')
        elif self.opc == 'VideoRecord':
            btn_path = Gtk.Button(label='Guardar video como')
        btn_path.connect("clicked", self.evt_path)
        box_data.pack_start(btn_path, True, True, 0)
        self.pth = ''


        crf_box = Gtk.Box(spacing=4)
        box_data.pack_start(crf_box, True, True, 0)

        self.crf_CheckButton = Gtk.CheckButton(label='Calidad (CRF de 0-50)')
        self.crf_CheckButton.set_active(True)
        crf_box.pack_start(self.crf_CheckButton, False, False, 0)

        crf_SpinButton_adj = Gtk.Adjustment(
                                upper=50, step_increment=1, page_increment=10, 
                                value=30
                             )
        self.crf_SpinButton = Gtk.SpinButton()
        self.crf_SpinButton.set_adjustment(crf_SpinButton_adj)
        self.crf_SpinButton.set_numeric(True)
        crf_box.pack_start(self.crf_SpinButton, False, False, 8)
        

        fps_box = Gtk.Box(spacing=4)
        box_data.pack_start(fps_box, True, True, 0)
        
        self.fps_CheckButton = Gtk.CheckButton(label='Fotogramas (FPS)')
        self.fps_CheckButton.set_active(True)
        fps_box.pack_start(self.fps_CheckButton, False, False, 0)
        
        self.fps_SpinButton = Gtk.SpinButton()
        fps_SpinButton_adj = Gtk.Adjustment(
            step_increment=1, page_increment=10
        )
        self.fps_SpinButton.set_adjustment(fps_SpinButton_adj)
        self.fps_SpinButton.set_range(1, 100)
        self.fps_SpinButton.set_value(25)
        self.fps_SpinButton.set_numeric(True)
        fps_box.pack_start(self.fps_SpinButton, False, False, 34)
        
        
        rez_box = Gtk.Box(spacing=4)
        box_data.pack_start(rez_box, True, True, 0)
        
        self.rez_CheckButton = Gtk.CheckButton(label='Resolucion (H x V)')
        self.rez_CheckButton.set_active(True)
        rez_box.pack_start(self.rez_CheckButton, False, False, 0)
        
        self.rez_entryH = Gtk.Entry()
        self.rez_entryH.set_text('1280')
        self.rez_entryH.set_width_chars(8)
        rez_box.pack_start(self.rez_entryH, False, False, 0)
        
        rez_label_HxV = Gtk.Label(label='x')
        rez_box.pack_start(rez_label_HxV, False, False, 0)
        
        self.rez_entryV = Gtk.Entry()
        self.rez_entryV.set_text('720')
        self.rez_entryV.set_width_chars(8)
        rez_box.pack_start(self.rez_entryV, False, False, 0)
        
        if self.opc == 'VideoRecord':
            preset_box = Gtk.Box(spacing=4)
            box_data.pack_start(preset_box, True, True, 0)
            
            self.preset_CheckButton = Gtk.CheckButton(label='Uso de CPU')
            self.preset_CheckButton.set_active(True)
            preset_box.pack_start(self.preset_CheckButton, False, False, 0)
            
            preset_ListStore = Gtk.ListStore(str)
            presets = [
                '-preset ultrafast',
                '-preset superfast',
                '-preset veryfast',
                '-preset faster',
                '-preset fast',
                '-preset medium',
                '-preset slow',
                '-preset slower',
                '-preset veryslow',
            ]
            for preset in presets:
                preset_ListStore.append([preset])
                
            self.preset_ComboBox = Gtk.ComboBox.new_with_model(preset_ListStore)
            preset_CellRendererText = Gtk.CellRendererText()
            self.preset_ComboBox.pack_start(preset_CellRendererText, True)
            self.preset_ComboBox.add_attribute(preset_CellRendererText, "text", 0)
            self.preset_ComboBox.set_active(5)
            preset_box.pack_start(self.preset_ComboBox, False, False, 16)
            
        else: self.preset_ComboBox = ''
        
        
        self.label_path = Gtk.Label()
        self.label_path.set_markup('<b>(Aqui se mostrara el Video)</b>')
        self.label_path.set_line_wrap(True)
        box_data.pack_start(self.label_path, True, True, 0)
        
        self.label_cfg = Gtk.Label()
        self.label_cfg.set_line_wrap(True)
        self.label_cfg.set_selectable(True)
        box_data.pack_start(self.label_cfg, True, True, 0)
        
        btn_add_cfg = Gtk.Button(label=self.txt_title)
        btn_add_cfg.connect('clicked', self.evt_add_cfg)
        box_data.pack_start(btn_add_cfg, True, True, 4)
        
        box_main = self.get_content_area()
        box_main.add(box_data)
        self.show_all()
        
    def evt_add_cfg(self, widget):
        Util.CleanScreen()
        
        if self.crf_CheckButton.get_active() == True:
            crf = FFmpeg.CRF(self.crf_SpinButton.get_value_as_int())
        else: crf = ''
            
        if self.fps_CheckButton.get_active() == True:
            fps = FFmpeg.FPS(self.fps_SpinButton.get_value_as_int())
        else: fps = ''
            
        if self.rez_CheckButton.get_active() == True:
            rez_HxV = FFmpeg.Resolution(
                rez_H=self.rez_entryH.get_text(), 
                rez_V=self.rez_entryV.get_text()
            )
        else: rez_HxV = ''
        
        try:
            preset_iter = self.preset_ComboBox.get_active_iter()
            preset_model = self.preset_ComboBox.get_model()
            preset = preset_model[preset_iter][0]
        except:
            preset = 'Sin preset'
        
        if self.pth == '': print('No se a seleccionado el Video')
        else:
            print(
                f'{preset}\n'
                f'Video seleccionado: "{self.pth}\n"'
                f'El CRF sera "{crf}"\n'
                f'Los FPS seran "{fps}"\n'
                f'La resolución sera "{rez_HxV}"'
            )
            
            if self.opc == 'VideoCompress':
                self.cfg = (
                    f'ffmpeg -i "{self.pth}" {crf} {fps} {rez_HxV} '
                    f'"{self.pth}_Comprimido.mkv"'
                )
            elif self.opc == 'VideoRecord':
                self.cfg = (
                    f'ffmpeg -f x11grab -i :0 {crf} {preset} {fps} '
                    f'{rez_HxV} "{self.pth}.mkv"'
                )
                txt=''
            
            self.label_cfg.set_markup(
                f'<small><i>{self.cfg}</i></small>'
            )
            
            dialog = Command_Run(self, cfg=self.cfg, txt=self.txt_title)
            rsp = dialog.run()
            dialog.destroy()
            #dialog = Gtk.MessageDialog(
            #    transient_for=self,
            #    flags=0,
            #    message_type=Gtk.MessageType.QUESTION,
            #    buttons=Gtk.ButtonsType.YES_NO,
            #    text=self.txt_title
            #)
            #dialog.format_secondary_text(self.cfg)
            #rsp = dialog.run()
            #if rsp == Gtk.ResponseType.YES:
            #    os.system(f"xfce4-terminal --startup-id= -e '{self.cfg}'")
            #elif rsp == Gtk.ResponseType.NO:
            #    print('NO Precionado')
            #dialog.destroy()
        
            
    def evt_path(self, widget):
        if self.opc == 'VideoRecord':
            dialog = Gtk.FileChooserDialog(
                title='Guardar video como', parent=self,
                action=Gtk.FileChooserAction.SAVE
            )
            dialog.add_buttons(
                Gtk.STOCK_CANCEL,
                Gtk.ResponseType.CANCEL,
                Gtk.STOCK_SAVE,
                Gtk.ResponseType.OK,
            )
        elif self.opc == 'VideoCompress':    
            dialog = Gtk.FileChooserDialog(
                title='Porfavor elige un video', parent=self,
                action=Gtk.FileChooserAction.OPEN
            )
            dialog.add_buttons(
                Gtk.STOCK_CANCEL,
                Gtk.ResponseType.CANCEL,
                Gtk.STOCK_OPEN,
                Gtk.ResponseType.OK,
            )
        
        self.add_flt(dialog)
            
        rsp = dialog.run()
        if rsp == Gtk.ResponseType.OK:
            self.pth = dialog.get_filename()
            self.label_path.set_text(f'Archivo: {self.pth}')
            print('Video Agregado')
            
        elif rsp == Gtk.ResponseType.CANCEL:
            self.cfg = ''
            print('Cancelar clickeado')
            
        dialog.destroy()
        
    def add_flt(self, dialog):
        flt_video = Gtk.FileFilter()
        flt_video.set_name("Archivos de Video")
        flt_video.add_mime_type("video/*")
        dialog.add_filter(flt_video)
        
            

class Window_Main(Gtk.Window):
    def __init__(self):
        super().__init__(title='Ventana Main')
        self.set_resizable(False)
        self.set_default_size(224, 128)
        
        box_v = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        
        label_title = Gtk.Label()
        label_title.set_markup('<b>Opciones</b>\n')

        box_v.pack_start(label_title, True, True, 8)

        btn_ffmpeg_compress = Gtk.Button(label='Comprimir videos')
        btn_ffmpeg_compress.connect("clicked", self.evt_ffmpeg_compress)
        box_v.pack_start(btn_ffmpeg_compress, True, True, 0)
        
        btn_ffmpeg_record = Gtk.Button(label='Grabar')
        btn_ffmpeg_record.connect("clicked", self.evt_ffmpeg_record)
        box_v.pack_start(btn_ffmpeg_record, True, True, 0)
        
        btn_txt_view = Gtk.Button(label='Ver comandos creados')
        btn_txt_view.connect("clicked", self.evt_text_view)
        box_v.pack_start(btn_txt_view, True, True, 0)

        btn_exit = Gtk.Button(label='Salir')
        btn_exit.connect("clicked", self.evt_exit)
        box_v.pack_start(btn_exit, True, True, 0)
        
        self.add(box_v)
        
    def evt_ffmpeg_compress(self, widget):
        dialog = Dialog_FFmpegVideo(self, opc='VideoCompress')
        response = dialog.run()
        dialog.destroy()
        print('Comprimir videos')
        
    def evt_ffmpeg_record(self, widget):
        dialog = Dialog_FFmpegVideo(self, opc='VideoRecord')
        response = dialog.run()
        dialog.destroy()
        print('Grabar Audio o video')
        
    def evt_text_view(self, widget):
        print('Abrir archivo de texto')
        
    def evt_exit(self, widget):
        exit()
        

win = Window_Main()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
