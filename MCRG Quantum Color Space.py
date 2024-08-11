import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QLineEdit, QLabel
from PyQt5.QtGui import QColor, QPainter, QPen, QImage, QPixmap
from PyQt5.QtCore import Qt, QPoint
import numpy as np


class TwoQubitState:
    def __init__(self, amplitudes):
        self.amplitudes = np.array([complex(a) for a in amplitudes])
        self.normalize()

    def normalize(self):
        norm = np.linalg.norm(self.amplitudes)
        if norm != 0:
            self.amplitudes /= norm

    def get_probabilities(self):
        return np.abs(self.amplitudes)**2

    def get_phases(self):
        return np.angle(self.amplitudes)

    def apply_gate(self, gate):
        self.amplitudes = np.dot(gate, self.amplitudes)
        self.normalize()

# Example quantum gates
H = np.array([[1, 1], [1, -1]]) / np.sqrt(2)  # Hadamard gate
CNOT = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]]) 
    
class QuantumVisualizer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Quantum State Visualizer')
        self.setGeometry(100, 100, 1000, 1000)  # Increased from 800x800 to 1000x1000

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        input_layout = QHBoxLayout()
        self.amplitude_inputs = [QLineEdit() for _ in range(4)]
        for i, input_field in enumerate(self.amplitude_inputs):
            input_field.setPlaceholderText(f'|{i:02b}⟩ amplitude')
            input_layout.addWidget(input_field)

        visualize_button = QPushButton('Visualize')
        visualize_button.clicked.connect(self.visualize)
        input_layout.addWidget(visualize_button)

        layout.addLayout(input_layout)

        self.state_label = QLabel()
        layout.addWidget(self.state_label)

        self.canvas = QuantumStateCanvas()
        layout.addWidget(self.canvas)

    def visualize(self):
        try:
            amplitudes = [complex(input_field.text()) for input_field in self.amplitude_inputs]
            state = TwoQubitState(amplitudes)
            self.state_label.setText(f'State: {state.amplitudes}')
            self.canvas.plot_state(state)
        except ValueError:
            self.state_label.setText('Invalid input. Please enter valid complex numbers (e.g., 1+2j).')

class QuantumStateCanvas(QWidget):
    def __init__(self):
        super().__init__()
        self.state = None

    def plot_state(self, state):
        self.state = state
        self.update()

    def paintEvent(self, event):
        if self.state is None:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        width = self.width()
        height = self.height()
        margin = 50

        # Draw color space
        self.draw_color_space(painter, width, height, margin)

        # Draw coordinate system and labels
        self.draw_coordinates_and_labels(painter, width, height, margin)

        # Draw quantum state
        self.draw_quantum_state(painter, width, height, margin)

        # Draw color representation of quantum state
        self.draw_quantum_color(painter, width, height, margin)

    def draw_color_space(self, painter, width, height, margin):
        for x in range(margin, width - margin):
            for y in range(margin, height - margin):
                normalized_x = (x - margin) / (width - 2 * margin)
                normalized_y = (height - y - margin) / (height - 2 * margin)
                
                r = int(255 * normalized_x)
                g = int(255 * normalized_y)
                b = int(255 * (1 - max(normalized_x, normalized_y)))
                
                painter.setPen(QColor(r, g, b))
                painter.drawPoint(x, y)

    def draw_coordinates_and_labels(self, painter, width, height, margin):
        painter.setPen(QPen(Qt.black, 2))
        painter.drawLine(margin, height - margin, width - margin, height - margin)
        painter.drawLine(margin, height - margin, margin, margin)

        # Label axes
        painter.drawText(width - margin + 5, height - margin + 15, 'R')
        painter.drawText(margin - 15, margin - 5, 'G')

        # Add number labels
        for i in range(0, 256, 64):
            x = margin + (width - 2 * margin) * i / 255
            y = height - margin - (height - 2 * margin) * i / 255
            painter.drawText(int(x), height - margin + 15, str(i))
            painter.drawText(margin - 30, int(y), str(i))

        self.label_color_space(painter, width, height, margin)

    def label_color_space(self, painter, width, height, margin):
        painter.setPen(Qt.black)
        font = painter.font()
        font.setPointSize(8)  # Reduce font size for better fit
        painter.setFont(font)
        
        # Bottom left
        painter.drawText(margin, height - margin + 15, "|00⟩")
        
        # Top left
        painter.drawText(margin, margin + 15, "|01⟩")
        
        # Bottom right
        painter.drawText(width - margin - 30, height - margin + 15, "|10⟩")
        
        # Top right
        painter.drawText(width - margin - 30, margin + 15, "|11⟩")

    def draw_quantum_state(self, painter, width, height, margin):
        probabilities = self.state.get_probabilities()
        phases = self.state.get_phases()
        colors = [QColor(0, 0, 255), QColor(0, 255, 0), QColor(255, 0, 0), QColor(255, 255, 0)]
        
        for i, (prob, phase, color) in enumerate(zip(probabilities, phases, colors)):
            x = int(margin + (width - 2 * margin) * (i % 2))
            y = int(height - margin - (height - 2 * margin) * (i // 2))
            
            # Draw probability circle
            painter.setPen(Qt.black)
            painter.setBrush(color)
            radius = int(min(50, 100 * np.sqrt(prob)))  # Limit max size and ensure it's an integer
            painter.drawEllipse(QPoint(x, y), radius, radius)
            
            # Draw phase arrow
            phase_x = int(x + radius * np.cos(phase))
            phase_y = int(y - radius * np.sin(phase))
            painter.drawLine(x, y, phase_x, phase_y)
            
            # Adjust text position based on which quadrant it's in
            text_x = x + 10 if i % 2 == 0 else x - 100
            text_y = y + 20 if i < 2 else y - 10
            
            painter.drawText(text_x, text_y, f'|{i:02b}⟩: {prob:.3f}, ∠{phase:.2f}')

    def draw_quantum_color(self, painter, width, height, margin):
        color = self.state_to_color(self.state)
        
        # Draw a rectangle with the state color
        painter.setBrush(color)
        painter.setPen(Qt.NoPen)
        painter.drawRect(width - 150, height - 150, 100, 100)
        
        # Label the color
        painter.setPen(Qt.black)
        painter.drawText(width - 150, height - 160, "State Color")

        # Display the hex code
        hex_code = f"#{color.red():02x}{color.green():02x}{color.blue():02x}"
        painter.drawText(width - 150, height - 40, f"Hex: {hex_code}")
        
    def state_to_color(self, state):
        # Calculate color components using complex arithmetic
        r = abs(state.amplitudes[0] + state.amplitudes[2])**2
        g = abs(state.amplitudes[1] + state.amplitudes[3])**2
        b = abs(state.amplitudes[0] + state.amplitudes[1])**2
        
        # Normalize
        max_val = max(r, g, b)
        if max_val > 0:
            r, g, b = r/max_val, g/max_val, b/max_val
        
        # Convert to RGB color
        return QColor(int(r*255), int(g*255), int(b*255))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = QuantumVisualizer()
    ex.show()
    sys.exit(app.exec_())
