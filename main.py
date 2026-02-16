# -*- coding: utf-8 -*-
import os
import json
import webbrowser
import threading
from pathlib import Path
import sys
import io
import weakref
from typing import List, Dict, Any, Callable, Optional
from functools import lru_cache

# Kivy 설정
from kivy.config import Config
Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '700')
Config.set('graphics', 'resizable', False)
Config.set('kivy', 'show_loadingscreen', '0')
Config.set('kivy', 'loading_image', '')

# 한글 인코딩 설정
try:
    sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')
except:
    pass

# 나머지 임포트
import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.togglebutton import ToggleButton
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.logger import Logger
from kivy.utils import platform
from kivy.animation import Animation

# 안드로이드 네이티브 컨텍스트 메뉴 사용 설정
if platform == 'android':
    Window.softinput_mode = 'below_target'

# Kivy 한글 폰트 설정
from kivy.core.text import LabelBase
from kivy.resources import resource_add_path

# 안드로이드 환경 확인
IS_ANDROID = platform == 'android'

# 안드로이드 저장소 경로 최적화
if IS_ANDROID:
    try:
        from android.storage import app_storage_path
        from android.permissions import request_permissions, Permission
        
        request_permissions([Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE])
        DATA_DIR = Path(app_storage_path()) / 'data'
    except:
        try:
            from android.storage import primary_external_storage_path
            storage_path = primary_external_storage_path()
            DATA_DIR = Path(storage_path) / 'sannaeeum'
        except:
            DATA_DIR = Path('/sdcard/sannaeeum')
else:
    DATA_DIR = Path.cwd() / 'data'

DATA_DIR.mkdir(exist_ok=True, parents=True)

# ============================================================
# 마루부리 폰트 설정
# ============================================================
FONT_NAME = 'MaruBuri'
FONT_PATH = 'res/fonts/MaruBuri-Bold.ttf'
KOREAN_FONT_AVAILABLE = False

try:
    if os.path.exists(FONT_PATH):
        font_dir = os.path.dirname(FONT_PATH)
        if font_dir:
            resource_add_path(font_dir)
        
        font_file = os.path.basename(FONT_PATH)
        LabelBase.register(name=FONT_NAME, fn_regular=font_file)
        KOREAN_FONT_AVAILABLE = True
        print(f"✅ 마루부리 폰트 등록 성공: {FONT_PATH}")
    else:
        print(f"⚠️ 마루부리 폰트를 찾을 수 없습니다: {FONT_PATH}")
        
        if IS_ANDROID:
            system_fonts = [
                '/system/fonts/NotoSansCJK-Regular.ttc',
                '/system/fonts/NotoSansKR-Regular.otf',
                '/system/fonts/DroidSansFallback.ttf'
            ]
            for sys_font in system_fonts:
                if os.path.exists(sys_font):
                    resource_add_path(os.path.dirname(sys_font))
                    LabelBase.register(name=FONT_NAME, fn_regular=os.path.basename(sys_font))
                    KOREAN_FONT_AVAILABLE = True
                    print(f"✅ 시스템 폰트로 대체: {sys_font}")
                    break
except Exception as e:
    print(f"⚠️ 폰트 등록 실패: {e}")
    KOREAN_FONT_AVAILABLE = False

def get_font_name():
    return FONT_NAME if KOREAN_FONT_AVAILABLE else None

# ============================================================
# 색상 정의 (완전히 동일 유지)
# ============================================================
COLORS = {
    'primary': '#8B5FBF',
    'primary_light': '#9D76C7',
    'primary_dark': '#6A4A8C',
    'secondary': '#D4BFFF',
    'accent': '#C8A2C8',
    'danger': '#FF6B6B',
    'warning': '#FFA726',
    'success': '#66BB6A',
    'green': '#2E7D32',
    'gold': '#FFD700',
    'background': '#F5F0FF',
    'text_primary': '#2D1B4E',
    'text_secondary': '#5D4A7A',
    'white': '#FFFFFF',
    'pink': '#FF69B4',
    'link_blue': '#1E40AF',
    'category_text': '#4C1D95',
    'description_text': '#2D1B4E'
}

CATEGORIES = {
    '0': '분류안함',
    '1': '교육',
    '2': '아이디어',
    '3': '생활',
    '4': '농업',
    '5': '쇼핑',
    '6': '여행',
    '7': '비즈니스',
    '8': '건강',
    '9': '가정',
    '10': '커뮤니티'
}

def hex_to_rgb(hex_color, alpha=1.0):
    hex_color = hex_color.lstrip('#')
    if len(hex_color) == 6:
        r = int(hex_color[0:2], 16) / 255.0
        g = int(hex_color[2:4], 16) / 255.0
        b = int(hex_color[4:6], 16) / 255.0
        return (r, g, b, alpha)
    return (1, 1, 1, 1)

# ============================================================
# Clock 이벤트 관리자 (메모리 누수 방지)
# ============================================================
class ClockManager:
    """Clock 이벤트를 중앙에서 관리하는 매니저 클래스"""
    _instance = None
    _events: List[Any] = []
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    @classmethod
    def schedule_once(cls, callback: Callable, timeout: float = 0) -> Any:
        """단일 실행 이벤트 예약"""
        def wrapped_callback(dt):
            try:
                callback(dt)
            except Exception as e:
                Logger.error(f"Clock 콜백 오류: {e}")
        
        event = Clock.schedule_once(wrapped_callback, timeout)
        cls._events.append(event)
        return event
    
    @classmethod
    def cancel_event(cls, event: Any) -> None:
        """특정 이벤트 취소"""
        if event in cls._events:
            try:
                event.cancel()
                cls._events.remove(event)
            except:
                pass
    
    @classmethod
    def cancel_all(cls) -> None:
        """모든 예약된 이벤트 취소"""
        for event in cls._events[:]:
            try:
                event.cancel()
            except:
                pass
        cls._events.clear()

# ============================================================
# 검색 파서 (OR, AND, NOT 연산 지원)
# ============================================================
class SearchParser:
    """검색어 파서 - OR, AND, NOT 연산 지원"""
    
    PRECEDENCE = {'NOT': 3, 'AND': 2, 'OR': 1}
    
    @classmethod
    def tokenize(cls, query: str) -> List[str]:
        """검색어를 토큰으로 분리"""
        if not query or not query.strip():
            return []
        
        tokens = []
        i = 0
        length = len(query)
        
        while i < length:
            if query[i].isspace():
                i += 1
                continue
            
            if query[i] == '(':
                tokens.append('(')
                i += 1
                continue
            elif query[i] == ')':
                tokens.append(')')
                i += 1
                continue
            
            upper_query = query[i:].upper()
            if upper_query.startswith('OR'):
                tokens.append('OR')
                i += 2
                continue
            elif upper_query.startswith('AND'):
                tokens.append('AND')
                i += 3
                continue
            elif upper_query.startswith('NOT'):
                tokens.append('NOT')
                i += 3
                continue
            
            if query[i] == '"':
                j = i + 1
                while j < length and query[j] != '"':
                    j += 1
                if j < length:
                    tokens.append(query[i+1:j].strip())
                    i = j + 1
                else:
                    tokens.append(query[i+1:].strip())
                    i = length
            else:
                j = i
                while j < length and not query[j].isspace() and query[j] not in '()':
                    j += 1
                tokens.append(query[i:j].strip())
                i = j
        
        return [t for t in tokens if t]
    
    @classmethod
    def infix_to_postfix(cls, tokens: List[str]) -> List[str]:
        """중위 표기법을 후위 표기법으로 변환"""
        output = []
        stack = []
        
        for token in tokens:
            if token in ('OR', 'AND', 'NOT'):
                while (stack and stack[-1] != '(' and 
                       cls.PRECEDENCE.get(stack[-1], 0) >= cls.PRECEDENCE.get(token, 0)):
                    output.append(stack.pop())
                stack.append(token)
            elif token == '(':
                stack.append(token)
            elif token == ')':
                while stack and stack[-1] != '(':
                    output.append(stack.pop())
                if stack and stack[-1] == '(':
                    stack.pop()
            else:
                output.append(token.lower())
        
        while stack:
            output.append(stack.pop())
        
        return output
    
    @classmethod
    def create_search_function(cls, postfix_tokens: List[str]) -> Callable[[Dict[str, str]], bool]:
        """후위 표기법 토큰을 검색 함수로 변환"""
        if not postfix_tokens:
            return lambda link: True
        
        stack = []
        
        for token in postfix_tokens:
            if token == 'OR':
                if len(stack) < 2:
                    continue
                right = stack.pop()
                left = stack.pop()
                stack.append(lambda link, l=left, r=right: l(link) or r(link))
            elif token == 'AND':
                if len(stack) < 2:
                    continue
                right = stack.pop()
                left = stack.pop()
                stack.append(lambda link, l=left, r=right: l(link) and r(link))
            elif token == 'NOT':
                if len(stack) < 1:
                    continue
                operand = stack.pop()
                stack.append(lambda link, op=operand: not op(link))
            else:
                search_term = token.lower()
                stack.append(lambda link, term=search_term: (
                    term in link.get('title', '').lower() or
                    term in link.get('description', '').lower() or
                    term in link.get('url', '').lower()
                ))
        
        return stack[0] if stack else lambda link: False
    
    @classmethod
    def parse(cls, query: str) -> Callable[[Dict[str, str]], bool]:
        """검색어를 파싱하여 검색 함수 반환"""
        if not query or not query.strip():
            return lambda link: True
        tokens = cls.tokenize(query)
        postfix = cls.infix_to_postfix(tokens)
        return cls.create_search_function(postfix)

# ============================================================
# 키보드 대응 팝업 클래스 (66px 이동)
# ============================================================
class KeyboardAwarePopup(Popup):
    """키보드가 올라올 때 팝업 위치를 66px 조정하는 팝업 클래스"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.keyboard_offset = dp(66)
        self.original_y = None
        self.is_keyboard_visible = False
        self.active_input = None
        self._clock_events = []
        
        # 키보드 이벤트 바인딩
        Window.bind(on_keyboard=self.on_keyboard)
        Window.bind(on_keyboard_down=self.on_keyboard_down)
        self.bind(on_open=self.on_popup_open)
        self.bind(on_dismiss=self.on_popup_dismiss)
    
    def on_popup_open(self, instance):
        """팝업이 열릴 때 원래 위치 저장"""
        self.original_y = self.y
    
    def on_popup_dismiss(self, instance):
        """팝업 닫힐 때 정리"""
        Window.unbind(on_keyboard=self.on_keyboard)
        Window.unbind(on_keyboard_down=self.on_keyboard_down)
        for event in self._clock_events:
            ClockManager.cancel_event(event)
        self._clock_events.clear()
    
    def on_keyboard_down(self, window, key, scancode, codepoint, modifier):
        """키보드가 나타날 때"""
        if not self.is_keyboard_visible and self.active_input:
            self.is_keyboard_visible = True
            self.on_keyboard_show()
    
    def on_keyboard(self, window, key, scancode, codepoint, modifier):
        """키보드 이벤트 처리"""
        if key == 27 and self.is_keyboard_visible:  # Back button
            self.is_keyboard_visible = False
            self.on_keyboard_hide()
            return True
        return False
    
    def on_keyboard_show(self):
        """키보드가 나타날 때 팝업을 66px 위로 이동"""
        if self.original_y is None:
            self.original_y = self.y
        
        new_y = self.original_y + self.keyboard_offset
        
        # 화면 상단을 넘어가지 않도록 제한
        if new_y + self.height > Window.height:
            new_y = Window.height - self.height - dp(10)
        
        # 애니메이션으로 이동
        anim = Animation(y=new_y, duration=0.2)
        anim.start(self)
    
    def on_keyboard_hide(self):
        """키보드가 사라질 때 팝업 원위치"""
        if self.original_y is not None:
            anim = Animation(y=self.original_y, duration=0.2)
            anim.start(self)
    
    def on_input_focus(self, instance, value):
        """입력 필드 포커스 이벤트"""
        self.active_input = instance if value else None
        
        if value and not self.is_keyboard_visible:
            event = Clock.schedule_once(lambda dt: self.check_keyboard(), 0.1)
            self._clock_events.append(event)
    
    def check_keyboard(self):
        """포커스 후 키보드 상태 확인"""
        if not self.is_keyboard_visible:
            self.is_keyboard_visible = True
            self.on_keyboard_show()

# ============================================================
# 한글 컨텍스트 메뉴를 지원하는 TextInput 클래스
# ============================================================
class KoreanTextInput(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._clock_events = []
        
        if IS_ANDROID:
            self.use_handles = True
            self.long_press_time = 0.3
        
        self.is_long_press = False
        self.long_press_triggered = False
        self.last_touch_pos = (0, 0)
        self.context_popup = None
    
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.last_touch_pos = touch.pos
            self.is_long_press = False
            self.long_press_triggered = False
            
            for event in self._clock_events:
                ClockManager.cancel_event(event)
            self._clock_events.clear()
            
            event = ClockManager.schedule_once(self.on_long_press, 0.3)
            self._clock_events.append(event)
            
            if touch.is_double_tap:
                ClockManager.cancel_event(event)
                self._clock_events.remove(event)
                self.select_all()
                event = ClockManager.schedule_once(self.on_long_press, 0.2)
                self._clock_events.append(event)
                return True
        
        return super().on_touch_down(touch)
    
    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos):
            for event in self._clock_events:
                ClockManager.cancel_event(event)
            self._clock_events.clear()
        return super().on_touch_up(touch)
    
    def on_long_press(self, dt):
        if self.long_press_triggered:
            return
        
        self.long_press_triggered = True
        self.is_long_press = True
        
        if self.context_popup:
            self.context_popup.dismiss()
            self.context_popup = None
        
        event = Clock.schedule_once(lambda dt: self.show_context_menu(self.last_touch_pos), 0.05)
        self._clock_events.append(event)
    
    def show_context_menu(self, touch_pos):
        has_selection = bool(self.selection_text)
        
        menu_items = [
            ('잘라내기', self.cut, has_selection),
            ('복사', self.copy, has_selection),
            ('붙여넣기', self.paste, True),
            ('전체선택', self.select_all, True)
        ]
        
        content = BoxLayout(
            orientation='horizontal',
            spacing=dp(5),
            size_hint=(None, None),
            padding=[dp(10), dp(5), dp(10), dp(5)]
        )
        
        for text, callback, enabled in menu_items:
            btn = Button(
                text=text,
                size_hint=(None, None),
                width=dp(90),
                height=dp(50),
                background_color=hex_to_rgb(COLORS['primary'] if enabled else '#999999'),
                background_normal='',
                color=hex_to_rgb(COLORS['white']),
                font_name=get_font_name(),
                font_size=dp(16),
                disabled=not enabled
            )
            
            def make_callback(cb):
                def wrapped(instance):
                    if not instance.disabled:
                        result = cb()
                        if self.context_popup:
                            self.context_popup.dismiss()
                            self.context_popup = None
                        return result
                return wrapped
            
            btn.bind(on_press=make_callback(callback))
            content.add_widget(btn)
        
        content.width = len(menu_items) * (dp(90) + dp(5)) + dp(20)
        content.height = dp(60)
        
        popup = Popup(
            title='',
            content=content,
            size_hint=(None, None),
            size=(content.width, content.height),
            background_color=hex_to_rgb(COLORS['primary_dark'], 0.95),
            auto_dismiss=True,
            separator_height=0,
            border=(0, 0, 0, 0)
        )
        
        popup_x = touch_pos[0] - content.width / 2
        popup_y = touch_pos[1] - content.height - dp(20)
        popup_x = max(dp(10), min(popup_x, Window.width - content.width - dp(10)))
        
        if popup_y < dp(10):
            popup_y = touch_pos[1] + dp(20)
            popup_y = min(popup_y, Window.height - content.height - dp(10))
        
        popup.pos = (popup_x, popup_y)
        popup.bind(on_dismiss=lambda x: setattr(self, 'context_popup', None))
        
        self.context_popup = popup
        popup.open()
    
    def paste(self):
        if IS_ANDROID:
            try:
                from jnius import autoclass
                PythonActivity = autoclass('org.kivy.android.PythonActivity')
                Context = autoclass('android.content.Context')
                
                context = PythonActivity.mActivity
                clipboard = context.getSystemService(Context.CLIPBOARD_SERVICE)
                
                if clipboard.hasPrimaryClip():
                    clip = clipboard.getPrimaryClip()
                    if clip and clip.getItemCount() > 0:
                        item = clip.getItemAt(0)
                        text = item.getText()
                        if text:
                            self.insert_text(str(text))
                            return True
            except:
                try:
                    from android import clipboard
                    text = clipboard.get_clipboard_text()
                    if text:
                        self.insert_text(text)
                        return True
                except:
                    try:
                        from kivy.core.clipboard import Clipboard
                        text = Clipboard.paste()
                        if text:
                            self.insert_text(text)
                            return True
                    except:
                        pass
        else:
            try:
                return super().paste()
            except:
                try:
                    from kivy.core.clipboard import Clipboard
                    text = Clipboard.paste()
                    if text:
                        self.insert_text(text)
                        return True
                except:
                    pass
        return False
    
    def cut(self):
        if self.selection_text:
            text = self.selection_text
            
            if IS_ANDROID:
                try:
                    from jnius import autoclass
                    PythonActivity = autoclass('org.kivy.android.PythonActivity')
                    Context = autoclass('android.content.Context')
                    
                    context = PythonActivity.mActivity
                    clipboard = context.getSystemService(Context.CLIPBOARD_SERVICE)
                    ClipData = autoclass('android.content.ClipData')
                    clip = ClipData.newPlainText('label', text)
                    clipboard.setPrimaryClip(clip)
                except:
                    try:
                        from android import clipboard
                        clipboard.set_clipboard_text(text)
                    except:
                        from kivy.core.clipboard import Clipboard
                        Clipboard.copy(text)
            else:
                from kivy.core.clipboard import Clipboard
                Clipboard.copy(text)
            
            self.delete_selection()
            return True
        return False
    
    def copy(self):
        if self.selection_text:
            text = self.selection_text
            
            if IS_ANDROID:
                try:
                    from jnius import autoclass
                    PythonActivity = autoclass('org.kivy.android.PythonActivity')
                    Context = autoclass('android.content.Context')
                    
                    context = PythonActivity.mActivity
                    clipboard = context.getSystemService(Context.CLIPBOARD_SERVICE)
                    ClipData = autoclass('android.content.ClipData')
                    clip = ClipData.newPlainText('label', text)
                    clipboard.setPrimaryClip(clip)
                except:
                    try:
                        from android import clipboard
                        clipboard.set_clipboard_text(text)
                    except:
                        from kivy.core.clipboard import Clipboard
                        Clipboard.copy(text)
            else:
                from kivy.core.clipboard import Clipboard
                Clipboard.copy(text)
            return True
        return False

# ============================================================
# 커스텀 위젯 클래스들 (디자인 완전히 동일 유지)
# ============================================================
class SimplePromotionButton(Button):
    def __init__(self, text, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_color = hex_to_rgb(COLORS['pink'])
        self.color = hex_to_rgb(COLORS['white'])
        self.size_hint_y = None
        self.height = dp(55)
        self.font_size = dp(20)
        self.bold = True
        self.text = text
        self.size_hint_x = 0.5
        self.padding = [dp(20), dp(10)]
        self.font_name = get_font_name()

class SimpleTitleLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.height = dp(80)
        self.padding = dp(10)
        self.spacing = dp(15)
        
        with self.canvas.before:
            Color(*hex_to_rgb(COLORS['primary']))
            self.rect = Rectangle(size=self.size, pos=self.pos)
        
        self.title_label = Label(
            text='산내음 링크 관리자',
            font_size=dp(24),
            bold=True,
            color=hex_to_rgb(COLORS['white']),
            size_hint_y=None,
            height=dp(60),
            font_name=get_font_name()
        )
        
        self.add_widget(self.title_label)
        self.bind(pos=self.update_rect, size=self.update_rect)
    
    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

class PurpleButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_color = hex_to_rgb(COLORS['primary'])
        self.color = hex_to_rgb(COLORS['white'])
        self.size_hint_y = None
        self.height = dp(50)
        self.font_size = dp(16)
        self.bold = True
        self.size_hint_x = 1.0
        self.padding = [dp(15), dp(10)]
        self.font_name = get_font_name()

class SmallButton(Button):
    def __init__(self, color_type='primary', **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.size_hint = (None, None)
        self.size = (dp(45), dp(45))
        self.font_size = dp(14)
        self.color = hex_to_rgb(COLORS['white'])
        
        if color_type == 'danger':
            self.background_color = hex_to_rgb(COLORS['danger'])
        elif color_type == 'warning':
            self.background_color = hex_to_rgb(COLORS['warning'])
        elif color_type == 'success':
            self.background_color = hex_to_rgb(COLORS['success'])
        else:
            self.background_color = hex_to_rgb(COLORS['primary'])
        
        self.font_name = get_font_name()

class CategoryToggleButton(ToggleButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_color = hex_to_rgb(COLORS['secondary'])
        self.background_color_down = hex_to_rgb(COLORS['primary'])
        self.color = hex_to_rgb(COLORS['text_primary'])
        self.size_hint_y = None
        self.height = dp(35)
        self.font_size = dp(13)
        self.group = 'categories'
        self.font_name = get_font_name()

class LinkCard(BoxLayout):
    def __init__(self, title, description, url, category, index, delete_callback, edit_callback, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.padding = [dp(15), dp(10), dp(5), dp(10)]
        self.spacing = dp(8)
        self.title = title
        self.url = url
        self.category = category
        self.index = index
        self.delete_callback = delete_callback
        self.edit_callback = edit_callback
        self._weak_ref = weakref.ref(self)
        
        with self.canvas.before:
            Color(*hex_to_rgb(COLORS['secondary'], 0.8))
            self.rect = RoundedRectangle(
                radius=[dp(15)] * 4,
                size=self.size,
                pos=self.pos
            )
        
        content_layout = BoxLayout(orientation='vertical', size_hint=(0.65, 1))
        font_name = get_font_name()
        
        title_label = Label(
            text=title,
            size_hint_y=None,
            height=dp(30),
            color=hex_to_rgb(COLORS['text_primary']),
            font_size=dp(18),
            bold=True,
            halign='left',
            font_name=font_name
        )
        title_label.bind(texture_size=title_label.setter('size'))
        
        desc_label = Label(
            text=description,
            size_hint_y=None,
            color=hex_to_rgb(COLORS['text_primary']),
            font_size=dp(14),
            text_size=(dp(350), None),
            halign='left',
            valign='top',
            font_name=font_name
        )
        desc_label.bind(texture_size=lambda i, v: setattr(i, 'height', max(v[1], dp(40))))
        
        short_url = url[:50] + "..." if len(url) > 50 else url
        url_label = Label(
            text=short_url,
            size_hint_y=None,
            height=dp(20),
            color=hex_to_rgb(COLORS['link_blue']),
            font_size=dp(12),
            halign='left',
            font_name=font_name
        )
        url_label.bind(texture_size=url_label.setter('size'))
        
        content_layout.add_widget(title_label)
        content_layout.add_widget(desc_label)
        content_layout.add_widget(url_label)
        
        right_layout = BoxLayout(orientation='vertical', size_hint=(0.3, 1), spacing=dp(5))
        
        category_label = Label(
            text=CATEGORIES.get(category, '분류안함'),
            size_hint_y=None,
            height=dp(25),
            color=hex_to_rgb(COLORS['white']),
            font_size=dp(13),
            bold=True,
            halign='center',
            valign='middle',
            font_name=font_name
        )
        
        with category_label.canvas.before:
            Color(*hex_to_rgb(COLORS['primary_dark']))
            self.category_bg = RoundedRectangle(
                radius=[dp(5)] * 4,
                size=category_label.size,
                pos=category_label.pos
            )
        
        category_label.bind(pos=self.update_category_bg, size=self.update_category_bg)
        
        button_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(45), spacing=dp(5))
        
        edit_btn = SmallButton(color_type='warning', text='✎')
        edit_btn.bind(on_press=self.edit_link)
        
        delete_btn = SmallButton(color_type='danger', text='X')
        delete_btn.bind(on_press=self.delete_link)
        
        button_layout.add_widget(edit_btn)
        button_layout.add_widget(delete_btn)
        
        right_layout.add_widget(category_label)
        right_layout.add_widget(button_layout)
        
        self.add_widget(content_layout)
        self.add_widget(right_layout)
        
        self.bind(pos=self.update_rect, size=self.update_rect)
        Clock.schedule_once(self.calculate_height, 0.1)
    
    def calculate_height(self, dt):
        base_height = self.padding[1] + self.padding[3] + self.spacing * 2
        content_height = 0
        if len(self.children) > 0:
            content_layout = self.children[1]
            for child in content_layout.children:
                content_height += child.height
        
        right_height = 0
        if len(self.children) > 0:
            right_layout = self.children[0]
            for child in right_layout.children:
                right_height += child.height
            right_height += right_layout.spacing * (len(right_layout.children) - 1)
        
        final_height = max(content_height, right_height) + base_height
        self.height = max(final_height, dp(100))
    
    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
    
    def update_category_bg(self, *args):
        if hasattr(self, 'category_bg'):
            self.category_bg.pos = self.children[0].children[1].pos
            self.category_bg.size = self.children[0].children[1].size
    
    def delete_link(self, instance):
        self.delete_callback(self.index)
    
    def edit_link(self, instance):
        self.edit_callback(self.index)
    
    def on_touch_down(self, touch):
        if len(self.children) > 0 and self.children[1].collide_point(*touch.pos):
            self.open_url_safe(self.url)
            return True
        return super().on_touch_down(touch)
    
    def open_url_safe(self, url):
        def _open():
            try:
                webbrowser.open(url)
            except Exception as e:
                Logger.error(f'LinkCard: URL 열기 실패: {e}')
        threading.Thread(target=_open).start()

# ============================================================
# 메인 앱 클래스
# ============================================================
class LinkApp(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = dp(15)
        self.spacing = dp(15)
        self.links = []
        self.displayed_links = []
        self.data_file = DATA_DIR / 'links.json'
        self.current_sort = 'title_asc'
        self.search_mode = False
        self.selected_category = 'all'
        self.current_page = 0
        self.page_size = 20
        self._refresh_trigger = None
        self.clock_manager = ClockManager()
        
        self.clock_manager.schedule_once(self.load_links, 0.1)
        self.clock_manager.schedule_once(self.setup_ui, 0.2)
        self.clock_manager.schedule_once(self.refresh_link_list, 0.3)
    
    def on_stop(self):
        """앱 종료 시 정리"""
        self.clock_manager.cancel_all()
        self.save_links()
    
    def load_links(self, dt=None):
        try:
            if self.data_file.exists():
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    loaded_links = json.load(f)
                    for link in loaded_links:
                        if 'category' not in link:
                            link['category'] = '0'
                    self.links = loaded_links
        except Exception as e:
            Logger.error(f'링크 로드 실패: {e}')
            self.links = []
    
    def setup_ui(self, dt=None):
        self.setup_promotion_buttons()
        
        title_layout = SimpleTitleLayout()
        self.add_widget(title_layout)
        
        self.setup_search_sort_ui()
        
        add_button = PurpleButton(text='+ 새 링크 추가')
        add_button.bind(on_press=self.show_add_link_popup)
        self.add_widget(add_button)
        
        self.setup_link_list()
    
    def setup_promotion_buttons(self):
        promotion_layout = BoxLayout(
            size_hint_y=None, 
            height=dp(60),
            spacing=dp(6),
            padding=[dp(0), dp(5), dp(0), dp(5)]
        )
        
        left_promo_btn = SimplePromotionButton(text='산내음청결고춧가루')
        left_promo_btn.bind(on_press=lambda x: self.open_url_safe('https://naver.me/5NqKupAN'))
        
        right_promo_btn = SimplePromotionButton(text='풀밭청결고춧가루')
        right_promo_btn.bind(on_press=lambda x: self.open_url_safe('https://naver.me/xaf7s1s5'))
        
        promotion_layout.add_widget(left_promo_btn)
        promotion_layout.add_widget(right_promo_btn)
        
        self.add_widget(promotion_layout)
    
    def open_url_safe(self, url):
        def _open():
            try:
                webbrowser.open(url)
            except Exception as e:
                Logger.error(f'URL 열기 실패: {e}')
        threading.Thread(target=_open).start()
    
    def setup_search_sort_ui(self):
        font_name = get_font_name()
        
        search_category_layout = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(6))
        
        self.search_input = KoreanTextInput(
            hint_text='검색어 (OR, AND, NOT 예: 바람 OR 김)',
            size_hint=(0.494, 1),
            background_color=hex_to_rgb(COLORS['white']),
            foreground_color=hex_to_rgb(COLORS['text_primary']),
            font_name=font_name
        )
        
        self.category_btn = Button(
            text='전체포함',
            size_hint=(0.184, 1),
            background_color=hex_to_rgb(COLORS['primary_light']),
            font_name=font_name
        )
        self.category_btn.bind(on_press=self.show_category_popup)
        
        search_btn = Button(
            text='검색',
            size_hint=(0.135, 1),
            background_color=hex_to_rgb(COLORS['primary']),
            font_name=font_name
        )
        search_btn.bind(on_press=self.search_links)
        
        clear_btn = Button(
            text='전체',
            size_hint=(0.135, 1),
            background_color=hex_to_rgb(COLORS['accent']),
            font_name=font_name
        )
        clear_btn.bind(on_press=self.clear_search)
        
        search_category_layout.add_widget(self.search_input)
        search_category_layout.add_widget(self.category_btn)
        search_category_layout.add_widget(search_btn)
        search_category_layout.add_widget(clear_btn)
        
        sort_layout = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(6))
        
        sort_buttons = [
            ('제목↑', 'title_asc'),
            ('제목↓', 'title_desc'),
            ('주소↑', 'url_asc'),
            ('주소↓', 'url_desc')
        ]
        
        for text, sort_type in sort_buttons:
            btn = Button(
                text=text,
                size_hint=(0.25, 1),
                background_color=hex_to_rgb(COLORS['primary_light']),
                font_name=font_name
            )
            btn.bind(on_press=lambda x, st=sort_type: self.sort_links(st))
            sort_layout.add_widget(btn)
        
        self.add_widget(search_category_layout)
        self.add_widget(sort_layout)
    
    def show_category_popup(self, instance):
        content = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(15))
        content.size_hint = (1, 1)
        
        font_name = get_font_name()
        
        title_label = Label(
            text='분류 선택',
            size_hint_y=None,
            height=dp(40),
            color=hex_to_rgb(COLORS['text_primary']),
            font_size=dp(18),
            bold=True,
            font_name=font_name
        )
        content.add_widget(title_label)
        
        scroll = ScrollView(do_scroll_x=False)
        category_layout = GridLayout(cols=1, size_hint_y=None, spacing=dp(5))
        category_layout.bind(minimum_height=category_layout.setter('height'))
        
        all_btn = CategoryToggleButton(text='전체 포함')
        all_btn.bind(on_press=lambda x: self.select_category('all'))
        if self.selected_category == 'all':
            all_btn.state = 'down'
        category_layout.add_widget(all_btn)
        
        for cat_id, cat_name in CATEGORIES.items():
            btn = CategoryToggleButton(text=f'{cat_id}. {cat_name}')
            btn.bind(on_press=lambda x, cid=cat_id: self.select_category(cid))
            if self.selected_category == cat_id:
                btn.state = 'down'
            category_layout.add_widget(btn)
        
        category_layout.height = len(CATEGORIES) * dp(35) + dp(40)
        scroll.add_widget(category_layout)
        content.add_widget(scroll)
        
        close_btn = Button(
            text='닫기',
            size_hint_y=None,
            height=dp(40),
            background_color=hex_to_rgb(COLORS['accent']),
            font_name=font_name
        )
        close_btn.bind(on_press=lambda x: popup.dismiss())
        content.add_widget(close_btn)
        
        popup = Popup(
            title='',
            content=content,
            size_hint=(0.8, 0.8),
            auto_dismiss=True
        )
        popup.open()
    
    def select_category(self, category_id):
        self.selected_category = category_id
        if category_id == 'all':
            self.category_btn.text = '전체포함'
        else:
            self.category_btn.text = f"{category_id}. {CATEGORIES.get(category_id, '분류안함')}"
        
        for child in self.children:
            if isinstance(child, Popup):
                child.dismiss()
                break
        
        self.refresh_link_list()
    
    def setup_link_list(self):
        self.scroll = ScrollView(do_scroll_x=False)
        self.link_layout = GridLayout(
            cols=1,
            size_hint_y=None,
            spacing=dp(15),
            padding=dp(10)
        )
        self.link_layout.bind(minimum_height=self.link_layout.setter('height'))
        
        self.scroll.add_widget(self.link_layout)
        self.add_widget(self.scroll)
    
    def refresh_link_list(self, dt=None):
        font_name = get_font_name()
        
        self.link_layout.clear_widgets()
        self.link_layout.height = 0
        
        links_to_display = self.displayed_links if self.search_mode else self.links
        
        if self.selected_category != 'all':
            links_to_display = [link for link in links_to_display if link.get('category', '0') == self.selected_category]
        
        if not links_to_display:
            empty_text = '검색 결과가 없습니다.' if self.search_mode else '저장된 링크가 없습니다.\n"새 링크 추가" 버튼을 눌러 추가하세요!'
            empty_label = Label(
                text=empty_text,
                size_hint_y=None,
                height=dp(100),
                color=hex_to_rgb(COLORS['text_secondary']),
                font_size=dp(16),
                halign='center',
                font_name=font_name
            )
            self.link_layout.add_widget(empty_label)
            self.link_layout.height += dp(100)
        else:
            start = self.current_page * self.page_size
            end = min(start + self.page_size, len(links_to_display))
            page_links = links_to_display[start:end]
            
            for i, link in enumerate(page_links):
                original_index = self.links.index(link) if link in self.links else (start + i)
                card = LinkCard(
                    link['title'], 
                    link['description'], 
                    link['url'], 
                    link.get('category', '0'),
                    original_index, 
                    self.delete_link, 
                    self.edit_link
                )
                self.link_layout.add_widget(card)
                Clock.schedule_once(lambda dt, c=card: self.update_card_height(c), 0.2)
            
            if end < len(links_to_display):
                more_btn = Button(
                    text='더 보기...',
                    size_hint_y=None,
                    height=dp(50),
                    background_color=hex_to_rgb(COLORS['primary_light']),
                    font_name=font_name
                )
                more_btn.bind(on_press=self.load_more)
                self.link_layout.add_widget(more_btn)
                self.link_layout.height += dp(50)
        
        Clock.schedule_once(lambda dt: setattr(self.scroll, 'scroll_y', 1), 0.1)
    
    def load_more(self, instance):
        self.current_page += 1
        self.refresh_link_list()
    
    def update_card_height(self, card):
        self.link_layout.height += card.height
    
    def search_links(self, instance):
        """개선된 검색 메서드 (SearchParser 사용)"""
        search_text = self.search_input.text.strip()
        self.current_page = 0
        
        try:
            search_func = SearchParser.parse(search_text)
            
            if not search_text:
                self.displayed_links = self.links.copy()
                self.search_mode = False
            else:
                self.displayed_links = [link for link in self.links if search_func(link)]
                self.search_mode = True
            
            self.sort_links(self.current_sort)
            
        except Exception as e:
            Logger.error(f'검색 중 오류: {e}')
            # 오류 발생 시 기본 검색으로 폴백
            self.fallback_search(search_text)
    
    def fallback_search(self, search_text):
        """기본 검색 (폴백)"""
        search_text_lower = search_text.lower()
        self.displayed_links = []
        
        for link in self.links:
            if (search_text_lower in link['title'].lower() or 
                search_text_lower in link['description'].lower() or 
                search_text_lower in link['url'].lower()):
                self.displayed_links.append(link)
        
        self.search_mode = True
        self.sort_links(self.current_sort)
    
    def clear_search(self, instance):
        self.search_input.text = ''
        self.selected_category = 'all'
        self.category_btn.text = '전체포함'
        self.search_mode = False
        self.current_page = 0
        self.refresh_link_list()
    
    def sort_links(self, sort_type):
        self.current_sort = sort_type
        links_to_sort = self.displayed_links if self.search_mode else self.links
        self.current_page = 0
        
        if sort_type == 'title_asc':
            links_to_sort.sort(key=lambda x: x['title'].lower())
        elif sort_type == 'title_desc':
            links_to_sort.sort(key=lambda x: x['title'].lower(), reverse=True)
        elif sort_type == 'url_asc':
            links_to_sort.sort(key=lambda x: x['url'].lower())
        elif sort_type == 'url_desc':
            links_to_sort.sort(key=lambda x: x['url'].lower(), reverse=True)
        
        self.refresh_link_list()
    
    @lru_cache(maxsize=128)
    def normalize_url(self, url):
        url = url.strip().lower()
        if url and not url.startswith(('http://', 'https://')):
            url = f'https://{url}'
        return url
    
    def check_duplicate_url(self, url):
        normalized_url = self.normalize_url(url)
        duplicate_indices = []
        for i, link in enumerate(self.links):
            existing_url = self.normalize_url(link['url'])
            if existing_url == normalized_url:
                duplicate_indices.append(i)
        return duplicate_indices
    
    def count_duplicate_urls(self, url):
        normalized_url = self.normalize_url(url)
        count = 0
        for link in self.links:
            existing_url = self.normalize_url(link['url'])
            if existing_url == normalized_url:
                count += 1
        return count
    
    def show_duplicate_popup(self, title, description, url, category, duplicate_indices):
        content = BoxLayout(orientation='vertical', spacing=dp(15), padding=dp(20))
        content.size_hint = (1, 1)
        
        font_name = get_font_name()
        current_duplicates = len(duplicate_indices)
        
        if current_duplicates >= 2:
            content.add_widget(Label(
                text=f'이미 같은 주소가 {current_duplicates}개 등록되어 있습니다.\n링크 주소 3개 이상 중복 등록 불가',
                color=hex_to_rgb(COLORS['white']),
                font_size=dp(16),
                size_hint_y=None,
                height=dp(80),
                font_name=font_name,
                text_size=(None, None),
                halign='center'
            ))
            
            button_layout = BoxLayout(spacing=dp(10), size_hint_y=None, height=dp(50))
            ok_btn = Button(text='확인', background_color=hex_to_rgb(COLORS['primary']), font_name=font_name)
            ok_btn.bind(on_press=lambda x: popup.dismiss())
            button_layout.add_widget(ok_btn)
            content.add_widget(button_layout)
            
            popup = Popup(
                title='',
                content=content,
                size_hint=(0.8, 0.5),
                auto_dismiss=False
            )
            popup.open()
            return
        
        content.add_widget(Label(
            text=f'이미 등록된 주소입니다:\n{self.links[duplicate_indices[0]]["title"]}',
            color=hex_to_rgb(COLORS['white']),
            font_size=dp(16),
            size_hint_y=None,
            height=dp(80),
            font_name=font_name,
            text_size=(None, None),
            halign='center'
        ))
        
        button_layout = BoxLayout(spacing=dp(10), size_hint_y=None, height=dp(50))
        
        buttons = [
            ('기존항목 지우고 등록', hex_to_rgb(COLORS['primary'])),
            ('취소', hex_to_rgb(COLORS['accent'])),
            ('중복 등록', hex_to_rgb(COLORS['warning']))
        ]
        
        for text, color in buttons:
            btn = Button(text=text, background_color=color, font_name=font_name)
            button_layout.add_widget(btn)
        
        duplicate_btn, cancel_btn, replace_btn = button_layout.children
        
        def duplicate_link(btn):
            self.add_link(title, description, url, category)
            popup.dismiss()
        
        def cancel_add(btn):
            popup.dismiss()
        
        def replace_link(btn):
            for index in sorted(duplicate_indices, reverse=True):
                del self.links[index]
            self.add_link(title, description, url, category)
            popup.dismiss()
        
        duplicate_btn.bind(on_press=duplicate_link)
        cancel_btn.bind(on_press=cancel_add)
        replace_btn.bind(on_press=replace_link)
        
        content.add_widget(button_layout)
        
        popup = Popup(
            title='',
            content=content,
            size_hint=(0.8, 0.5),
            auto_dismiss=False
        )
        popup.open()
    
    def show_add_link_popup(self, instance):
        """새 링크 추가 팝업 (KeyboardAwarePopup 사용)"""
        font_name = get_font_name()
        
        content = BoxLayout(
            orientation='vertical',
            spacing=dp(8),
            padding=[dp(15), dp(15), dp(15), dp(10)],
            size_hint_y=None,
            height=dp(382)
        )
        
        green_line = BoxLayout(size_hint_y=None, height=dp(5))
        with green_line.canvas.before:
            Color(*hex_to_rgb(COLORS['green']))
            green_line.rect = Rectangle(size=green_line.size, pos=green_line.pos)
        green_line.bind(pos=lambda i, p: setattr(i.rect, 'pos', p))
        green_line.bind(size=lambda i, s: setattr(i.rect, 'size', s))
        content.add_widget(green_line)
        
        title_label = Label(
            text='새 링크 추가',
            size_hint_y=None,
            height=dp(50),
            color=hex_to_rgb(COLORS['white']),
            font_size=dp(20),
            bold=True,
            valign='middle',
            halign='center',
            font_name=font_name
        )
        title_label.bind(size=title_label.setter('text_size'))
        content.add_widget(title_label)
        
        self.title_input = KoreanTextInput(
            hint_text='사이트 제목을 입력하세요',
            size_hint_y=None,
            height=dp(50),
            font_name=font_name
        )
        self.title_input.bind(focus=self.on_input_focus)
        content.add_widget(self.title_input)
        
        self.desc_input = KoreanTextInput(
            hint_text='사이트 설명을 입력하세요\n(여러 줄로 입력 가능)',
            size_hint_y=None,
            height=dp(80),
            multiline=True,
            font_name=font_name
        )
        self.desc_input.bind(focus=self.on_input_focus)
        content.add_widget(self.desc_input)
        
        self.url_input = KoreanTextInput(
            hint_text='https://example.com',
            size_hint_y=None,
            height=dp(50),
            font_name=font_name
        )
        self.url_input.bind(focus=self.on_input_focus)
        content.add_widget(self.url_input)
        
        button_layout = BoxLayout(spacing=dp(8), size_hint_y=None, height=dp(48))
        
        cancel_btn = Button(
            text='취소', 
            background_color=hex_to_rgb(COLORS['accent']),
            size_hint=(0.3, 1),
            font_name=font_name
        )
        
        self.category_select_btn = Button(
            text='0. 분류안함',
            size_hint=(0.4, 1),
            background_color=hex_to_rgb(COLORS['primary_light']),
            font_name=font_name
        )
        self.category_select_btn.bind(on_press=self.show_add_category_popup)
        
        save_btn = Button(
            text='저장', 
            background_color=hex_to_rgb(COLORS['primary']),
            size_hint=(0.3, 1),
            font_name=font_name
        )
        
        button_layout.add_widget(cancel_btn)
        button_layout.add_widget(self.category_select_btn)
        button_layout.add_widget(save_btn)
        content.add_widget(button_layout)
        
        self.selected_category_id = '0'
        
        def save_link(btn):
            title = self.title_input.text.strip()
            description = self.desc_input.text.strip()
            url = self.url_input.text.strip()
            
            if title and url:
                normalized_url = self.normalize_url(url)
                duplicate_indices = self.check_duplicate_url(normalized_url)
                if duplicate_indices:
                    popup.dismiss()
                    self.show_duplicate_popup(title, description, normalized_url, self.selected_category_id, duplicate_indices)
                else:
                    self.add_link(title, description, normalized_url, self.selected_category_id)
                    popup.dismiss()
        
        def close_popup(btn):
            popup.dismiss()
        
        save_btn.bind(on_press=save_link)
        cancel_btn.bind(on_press=close_popup)
        
        popup = KeyboardAwarePopup(
            title='',
            content=content,
            size_hint=(None, None),
            width=dp(360),
            height=dp(382),
            auto_dismiss=False
        )
        
        popup.on_input_focus = self.on_input_focus
        
        popup.open()
        Clock.schedule_once(lambda dt: setattr(self.title_input, 'focus', True), 0.2)
    
    def on_input_focus(self, instance, value):
        """입력 필드 포커스 이벤트 처리"""
        for child in self.walk():
            if isinstance(child, KeyboardAwarePopup):
                child.on_input_focus(instance, value)
                break
    
    def show_add_category_popup(self, instance):
        content = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(15))
        
        font_name = get_font_name()
        
        content.add_widget(Label(
            text='분류 선택',
            color=hex_to_rgb(COLORS['text_primary']),
            font_size=dp(18),
            bold=True,
            size_hint_y=None,
            height=dp(40),
            font_name=font_name
        ))
        
        scroll = ScrollView(do_scroll_x=False)
        category_layout = GridLayout(cols=1, size_hint_y=None, spacing=dp(5))
        category_layout.bind(minimum_height=category_layout.setter('height'))
        
        for cat_id, cat_name in CATEGORIES.items():
            btn = CategoryToggleButton(text=f'{cat_id}. {cat_name}')
            btn.bind(on_press=lambda x, cid=cat_id: self.select_add_category(cid, popup))
            if self.selected_category_id == cat_id:
                btn.state = 'down'
            category_layout.add_widget(btn)
        
        category_layout.height = len(CATEGORIES) * dp(35)
        scroll.add_widget(category_layout)
        content.add_widget(scroll)
        
        close_btn = Button(
            text='닫기',
            size_hint_y=None,
            height=dp(40),
            background_color=hex_to_rgb(COLORS['accent']),
            font_name=font_name
        )
        close_btn.bind(on_press=lambda x: popup.dismiss())
        content.add_widget(close_btn)
        
        popup = Popup(
            title='',
            content=content,
            size_hint=(0.7, 0.7),
            auto_dismiss=False
        )
        popup.open()
    
    def select_add_category(self, category_id, popup):
        self.selected_category_id = category_id
        self.category_select_btn.text = f'{category_id}. {CATEGORIES[category_id]}'
        popup.dismiss()
    
    def edit_link(self, index):
        """링크 수정 팝업 (KeyboardAwarePopup 사용)"""
        if index < 0 or index >= len(self.links):
            return
        
        link = self.links[index]
        font_name = get_font_name()
        
        content = BoxLayout(
            orientation='vertical',
            spacing=dp(8),
            padding=[dp(15), dp(15), dp(15), dp(10)],
            size_hint_y=None,
            height=dp(382)
        )
        
        green_line = BoxLayout(size_hint_y=None, height=dp(5))
        with green_line.canvas.before:
            Color(*hex_to_rgb(COLORS['green']))
            green_line.rect = Rectangle(size=green_line.size, pos=green_line.pos)
        green_line.bind(pos=lambda i, p: setattr(i.rect, 'pos', p))
        green_line.bind(size=lambda i, s: setattr(i.rect, 'size', s))
        content.add_widget(green_line)
        
        title_label = Label(
            text='기존 링크 수정',
            size_hint_y=None,
            height=dp(50),
            color=hex_to_rgb(COLORS['white']),
            font_size=dp(20),
            bold=True,
            valign='middle',
            halign='center',
            font_name=font_name
        )
        title_label.bind(size=title_label.setter('text_size'))
        content.add_widget(title_label)
        
        title_input = KoreanTextInput(
            text=link['title'],
            size_hint_y=None,
            height=dp(50),
            font_name=font_name
        )
        title_input.bind(focus=self.on_input_focus)
        content.add_widget(title_input)
        
        desc_input = KoreanTextInput(
            text=link['description'],
            size_hint_y=None,
            height=dp(80),
            multiline=True,
            font_name=font_name
        )
        desc_input.bind(focus=self.on_input_focus)
        content.add_widget(desc_input)
        
        url_input = KoreanTextInput(
            text=link['url'],
            size_hint_y=None,
            height=dp(50),
            font_name=font_name
        )
        url_input.bind(focus=self.on_input_focus)
        content.add_widget(url_input)
        
        button_layout = BoxLayout(spacing=dp(8), size_hint_y=None, height=dp(48))
        
        cancel_btn = Button(
            text='취소', 
            background_color=hex_to_rgb(COLORS['accent']),
            size_hint=(0.3, 1),
            font_name=font_name
        )
        
        current_category = link.get('category', '0')
        category_select_btn = Button(
            text=f'{current_category}. {CATEGORIES.get(current_category, "분류안함")}',
            size_hint=(0.4, 1),
            background_color=hex_to_rgb(COLORS['primary_light']),
            font_name=font_name
        )
        
        save_btn = Button(
            text='수정', 
            background_color=hex_to_rgb(COLORS['primary']),
            size_hint=(0.3, 1),
            font_name=font_name
        )
        
        button_layout.add_widget(cancel_btn)
        button_layout.add_widget(category_select_btn)
        button_layout.add_widget(save_btn)
        content.add_widget(button_layout)
        
        edit_selected_category = current_category
        
        def show_edit_category_popup(instance):
            edit_content = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(15))
            
            edit_content.add_widget(Label(
                text='분류 선택',
                color=hex_to_rgb(COLORS['text_primary']),
                font_size=dp(18),
                bold=True,
                size_hint_y=None,
                height=dp(40),
                font_name=font_name
            ))
            
            scroll = ScrollView(do_scroll_x=False)
            edit_category_layout = GridLayout(cols=1, size_hint_y=None, spacing=dp(5))
            edit_category_layout.bind(minimum_height=edit_category_layout.setter('height'))
            
            for cat_id, cat_name in CATEGORIES.items():
                btn = CategoryToggleButton(text=f'{cat_id}. {cat_name}')
                btn.bind(on_press=lambda x, cid=cat_id: select_edit_category(cid, edit_popup))
                if edit_selected_category == cat_id:
                    btn.state = 'down'
                edit_category_layout.add_widget(btn)
            
            edit_category_layout.height = len(CATEGORIES) * dp(35)
            scroll.add_widget(edit_category_layout)
            edit_content.add_widget(scroll)
            
            close_btn = Button(
                text='닫기',
                size_hint_y=None,
                height=dp(40),
                background_color=hex_to_rgb(COLORS['accent']),
                font_name=font_name
            )
            close_btn.bind(on_press=lambda x: edit_popup.dismiss())
            edit_content.add_widget(close_btn)
            
            edit_popup = Popup(
                title='',
                content=edit_content,
                size_hint=(0.7, 0.7),
                auto_dismiss=False
            )
            edit_popup.open()
        
        def select_edit_category(category_id, popup):
            nonlocal edit_selected_category
            edit_selected_category = category_id
            category_select_btn.text = f'{category_id}. {CATEGORIES[category_id]}'
            popup.dismiss()
        
        category_select_btn.bind(on_press=show_edit_category_popup)
        
        def save_edit(btn):
            new_title = title_input.text.strip()
            new_description = desc_input.text.strip()
            new_url = url_input.text.strip()
            
            if new_title and new_url:
                normalized_url = self.normalize_url(new_url)
                
                duplicate_indices = []
                for i, existing_link in enumerate(self.links):
                    if i != index:
                        existing_url = self.normalize_url(existing_link['url'])
                        if existing_url == normalized_url:
                            duplicate_indices.append(i)
                
                if duplicate_indices:
                    popup.dismiss()
                    self.show_edit_duplicate_popup(new_title, new_description, normalized_url, edit_selected_category, index, duplicate_indices)
                else:
                    self.update_link(index, new_title, new_description, normalized_url, edit_selected_category)
                    popup.dismiss()
        
        def cancel_edit(btn):
            popup.dismiss()
        
        save_btn.bind(on_press=save_edit)
        cancel_btn.bind(on_press=cancel_edit)
        
        popup = KeyboardAwarePopup(
            title='',
            content=content,
            size_hint=(None, None),
            width=dp(360),
            height=dp(382),
            auto_dismiss=False
        )
        
        popup.on_input_focus = self.on_input_focus
        
        popup.open()
        Clock.schedule_once(lambda dt: setattr(title_input, 'focus', True), 0.2)
    
    def show_edit_duplicate_popup(self, title, description, url, category, edit_index, duplicate_indices):
        content = BoxLayout(orientation='vertical', spacing=dp(15), padding=dp(20))
        
        font_name = get_font_name()
        current_duplicates = len(duplicate_indices)
        
        if current_duplicates >= 2:
            content.add_widget(Label(
                text=f'이미 같은 주소가 {current_duplicates}개 등록되어 있습니다.\n링크 주소 3개 이상 중복 등록 불가',
                color=hex_to_rgb(COLORS['white']),
                font_size=dp(16),
                size_hint_y=None,
                height=dp(80),
                font_name=font_name,
                halign='center'
            ))
            
            button_layout = BoxLayout(spacing=dp(10), size_hint_y=None, height=dp(50))
            ok_btn = Button(text='확인', background_color=hex_to_rgb(COLORS['primary']), font_name=font_name)
            ok_btn.bind(on_press=lambda x: popup.dismiss())
            button_layout.add_widget(ok_btn)
            content.add_widget(button_layout)
            
            popup = Popup(
                title='',
                content=content,
                size_hint=(0.8, 0.5),
                auto_dismiss=False
            )
            popup.open()
            return
        
        content.add_widget(Label(
            text=f'다른 항목에 같은 주소가 있습니다:\n{self.links[duplicate_indices[0]]["title"]}',
            color=hex_to_rgb(COLORS['white']),
            font_size=dp(16),
            size_hint_y=None,
            height=dp(80),
            font_name=font_name,
            halign='center'
        ))
        
        button_layout = BoxLayout(spacing=dp(10), size_hint_y=None, height=dp(50))
        
        buttons = [
            ('기존항목 유지', hex_to_rgb(COLORS['primary'])),
            ('취소', hex_to_rgb(COLORS['accent'])),
            ('기존항목 지우고 수정', hex_to_rgb(COLORS['warning']))
        ]
        
        for text, color in buttons:
            btn = Button(text=text, background_color=color, font_name=font_name)
            button_layout.add_widget(btn)
        
        keep_btn, cancel_btn, replace_btn = button_layout.children
        
        def keep_original(btn):
            self.update_link(edit_index, title, description, url, category)
            popup.dismiss()
        
        def cancel_edit(btn):
            popup.dismiss()
        
        def replace_and_edit(btn):
            for index in sorted(duplicate_indices, reverse=True):
                del self.links[index]
            adjusted_index = edit_index
            for dup_index in duplicate_indices:
                if dup_index < edit_index:
                    adjusted_index -= 1
            self.update_link(adjusted_index, title, description, url, category)
            popup.dismiss()
        
        keep_btn.bind(on_press=keep_original)
        cancel_btn.bind(on_press=cancel_edit)
        replace_btn.bind(on_press=replace_and_edit)
        
        content.add_widget(button_layout)
        
        popup = Popup(
            title='',
            content=content,
            size_hint=(0.8, 0.5),
            auto_dismiss=False
        )
        popup.open()
    
    def update_link(self, index, title, description, url, category):
        if 0 <= index < len(self.links):
            self.links[index] = {
                'title': title,
                'description': description,
                'url': url,
                'category': category
            }
            self.save_links()
            self.refresh_link_list()
    
    def delete_link(self, index):
        content = BoxLayout(orientation='vertical', spacing=dp(15), padding=dp(20))
        
        font_name = get_font_name()
        
        content.add_widget(Label(
            text=f'"{self.links[index]["title"]}" 링크를 삭제하시겠습니까?',
            color=hex_to_rgb(COLORS['white']),
            font_size=dp(16),
            size_hint_y=None,
            height=dp(60),
            font_name=font_name,
            halign='center'
        ))
        
        button_layout = BoxLayout(spacing=dp(10), size_hint_y=None, height=dp(50))
        cancel_btn = Button(text='취소', background_color=hex_to_rgb(COLORS['accent']), font_name=font_name)
        delete_btn = Button(text='삭제', background_color=hex_to_rgb(COLORS['danger']), font_name=font_name)
        
        def confirm_delete(btn):
            if 0 <= index < len(self.links):
                del self.links[index]
                self.save_links()
                self.refresh_link_list()
            popup.dismiss()
        
        def cancel_delete(btn):
            popup.dismiss()
        
        delete_btn.bind(on_press=confirm_delete)
        cancel_btn.bind(on_press=cancel_delete)
        
        button_layout.add_widget(cancel_btn)
        button_layout.add_widget(delete_btn)
        content.add_widget(button_layout)
        
        popup = Popup(
            title='',
            content=content,
            size_hint=(0.7, 0.4),
            auto_dismiss=False
        )
        popup.open()
    
    def add_link(self, title, description, url, category):
        new_link = {
            'title': title,
            'description': description,
            'url': url,
            'category': category
        }
        self.links.append(new_link)
        self.save_links()
        self.refresh_link_list()
    
    def save_links(self):
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.links, f, ensure_ascii=False, indent=2)
        except Exception as e:
            Logger.error(f'링크 저장 실패: {e}')

# ============================================================
# 앱 실행
# ============================================================
class SannaeeumLinkApp(App):
    def build(self):
        Window.clearcolor = hex_to_rgb(COLORS['background'])
        self.title = '산내음 링크'
        self.icon = 'icon.png'
        
        Window.bind(on_keyboard=self.on_keyboard)
        
        return LinkApp()
    
    def on_keyboard(self, window, key, scancode, codepoint, modifier):
        if key == 27:
            self.stop()
            return True
        return False
    
    def on_stop(self):
        """앱 종료 시 정리"""
        if hasattr(self, 'root') and self.root:
            if hasattr(self.root, 'on_stop'):
                self.root.on_stop()

if __name__ == '__main__':
    print("산내음 링크 앱 시작 중...")
    print(f"마루부리 폰트 사용 가능: {KOREAN_FONT_AVAILABLE}")
    print(f"데이터 저장 경로: {DATA_DIR}")
    try:
        SannaeeumLinkApp().run()
    except Exception as e:
        print(f"앱 실행 중 오류 발생: {e}")
        import traceback
        traceback.print_exc()
        if not IS_ANDROID:
            input("엔터 키를 누르면 종료됩니다...")