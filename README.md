# 📊 YT Trend Predictor

ระบบดึงข้อมูลและวิเคราะห์ทำนายโอกาสในการรักษาระดับความปังของวิดีโอติดเทรนด์บน YouTube (ประเทศไทย) แบบ On-Demand Real-Time โดยคำนวณจากความเร็วการพุ่งของยอดวิว ฐานความเหนียวแน่นของผู้ชม และประเภทของหมวดหมู่วิดีโอ

## 🚀 Features

- **Real-time Data Ingestion:** ดึงข้อมูลส่วนตัวเลขสถิติและเวลาอัปโหลดของวิดีโอติดเทรนด์อันดับ 1-50 ของไทยผ่าน YouTube Data API v3
- **Data Cleaning & Engineering:** แปลงหมวดหมู่ `Category_ID` เป็นชื่อสากล และทำ Feature Engineering คำนวณความเร็วยอดวิวต่อชั่วโมง (`Views_per_Hour`) แบบอัจฉริยะในทุกรอบการทำงาน
- **Exploratory Data Analysis (EDA):** มีระบบประมวลผลพ่นไฟล์ภาพกราฟสรุปพฤติกรรมเทรนด์อัตโนมัติลงในโฟลเดอร์ `plots/`
- **Predictor Engine:** ใช้โมเดลคณิตศาสตร์ถ่วงน้ำหนัก (Weighted Scoring Model) อิงตามค่า Percentiles สถิติจริง ณ เวลานั้น เพื่อทำนายโอกาสรอดหรือร่วงในหน้าเทรนด์ออกมาเป็นเปอร์เซ็นต์ (0-100%)

## 🛠️ Tech Stack & Libraries

- **Language:** Python
- **Data & Analytics:** Pandas, NumPy
- **Visualization:** Matplotlib, Seaborn
- **API Integration:** Google API Python Client

## 📁 Project Structure

- `test_fetch.py` - สคริปต์ดึงข้อมูล Real-time จาก API และจัดการโครงสร้างลงไฟล์ CSV
- `visualize_data.py` - สคริปต์ทำ Feature Engineering และวาดกราฟสรุปผล
- `predict_trend.py` - แกนหลักโมเดลทำนายเปอร์เซ็นต์โอกาสคงตัวบนหน้าเทรนด์ (เวอร์ชัน Defensive Code ป้องกันบั๊กคอลัมน์หาย)
- `data/` - โฟลเดอร์จัดเก็บคลังข้อมูลดิบดิบที่ดึงมา
- `plots/` - โฟลเดอร์เก็บรูปภาพกราฟสรุปผล Insights

## ⚙️ How to Run

1. ดึงข้อมูลล่าสุด: `python test_fetch.py`
2. อัปเดตกราฟสรุปผล: `python visualize_data.py`
3. ประมวลผลโมเดลทำนาย: `python predict_trend.py`
