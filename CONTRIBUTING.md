# Contributing to Advanced Hand Gesture Recognition

Cảm ơn bạn quan tâm đến việc đóng góp cho dự án! 🎉

## 🚀 Cách đóng góp

### 1. Báo cáo Bug
- Sử dụng GitHub Issues
- Mô tả chi tiết vấn đề
- Cung cấp steps to reproduce
- Đính kèm screenshots nếu có

### 2. Đề xuất tính năng mới
- Mở GitHub Issue với label "enhancement"
- Giải thích tại sao tính năng này hữu ích
- Mô tả cách implement (nếu có)

### 3. Code Contribution

#### Setup Development Environment
```bash
# Clone repo
git clone https://github.com/yourusername/advanced-hand-gesture-recognition.git
cd advanced-hand-gesture-recognition

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# hoặc
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

#### Code Style
- Sử dụng Python PEP 8
- Comment code bằng tiếng Việt hoặc tiếng Anh
- Tên biến/function có ý nghĩa
- Docstrings cho functions quan trọng

#### Testing
```bash
# Test basic functionality
python main.py

# Test advanced features
python advanced_main.py

# Test training mode
python gesture_trainer.py
```

### 4. Pull Request Process

1. **Fork** repository
2. **Create branch** từ `main`:
   ```bash
   git checkout -b feature/ten-tinh-nang-moi
   ```
3. **Make changes** và test kỹ
4. **Commit** với message rõ ràng:
   ```bash
   git commit -m "feat: thêm nhận diện cử chỉ wave"
   ```
5. **Push** to your fork:
   ```bash
   git push origin feature/ten-tinh-nang-moi
   ```
6. **Create Pull Request** với mô tả chi tiết

## 📋 Commit Message Convention

```
type(scope): description

feat: tính năng mới
fix: sửa bug
docs: cập nhật documentation
style: format code, không thay đổi logic
refactor: refactor code
test: thêm tests
chore: cập nhật build tools, dependencies
```

## 🎯 Areas for Contribution

### High Priority
- [ ] Thêm gesture mới (wave, circle, etc.)
- [ ] Cải thiện accuracy
- [ ] Tối ưu performance
- [ ] Mobile app version

### Medium Priority
- [ ] Web interface
- [ ] Custom gesture training
- [ ] Multi-language support
- [ ] Better UI/UX

### Low Priority
- [ ] Voice commands integration
- [ ] AR/VR support
- [ ] Cloud sync
- [ ] Analytics dashboard

## 🐛 Bug Report Template

```markdown
**Describe the bug**
Mô tả ngắn gọn về bug

**To Reproduce**
Steps to reproduce:
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

**Expected behavior**
Mô tả kết quả mong đợi

**Screenshots**
Nếu có, đính kèm screenshots

**Environment:**
 - OS: [e.g. Windows 10]
 - Python version: [e.g. 3.9]
 - OpenCV version: [e.g. 4.8.1]
 - Camera: [e.g. Built-in webcam]

**Additional context**
Thông tin bổ sung khác
```

## 💡 Feature Request Template

```markdown
**Is your feature request related to a problem?**
Mô tả vấn đề hiện tại

**Describe the solution you'd like**
Mô tả giải pháp mong muốn

**Describe alternatives you've considered**
Các phương án thay thế đã cân nhắc

**Additional context**
Screenshots, mockups, hoặc thông tin bổ sung
```

## 🏆 Recognition

Contributors sẽ được ghi nhận trong:
- README.md
- CONTRIBUTORS.md
- Release notes

## 📞 Contact

Có câu hỏi? Liên hệ:
- GitHub Issues
- Email: your.email@example.com
- Discord: [Server link]

---

**Cảm ơn bạn đã đóng góp! 🙏**