import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# 1. โหลดข้อมูลจากไฟล์ CSV ที่เราเซฟไว้
csv_path = "data/yt_trending_data.csv"
df = pd.read_csv(csv_path)

print("🛠️ กำลังทำ Feature Engineering และสร้างกราฟสรุปข้อมูล...")

# 2. FEATURE ENGINEERING: สร้างตัวแปรความเร็วของยอดวิว (Views per Hour)
df['Views_per_Hour'] = round(df['Views'] / df['Hours_Since_Published'], 1)

df.to_csv(csv_path, index=False, encoding="utf-8-sig")
print("✅ เพิ่มฟีเจอร์ 'Views_per_Hour' ลงใน CSV เรียบร้อย!")

# สร้างโฟลเดอร์สำหรับเก็บรูปภาพ
os.makedirs("plots", exist_ok=True)

# 3. VISUALIZATION 1: กราฟแท่งดูหมวดหมู่ยอดฮิตในหน้าเทรนด์
plt.figure(figsize=(10, 6))
sns.set_theme(style="whitegrid")
sns.countplot(data=df, y='Category', order=df['Category'].value_counts().index, palette='viridis')
plt.title('Top Categories in Thailand YouTube Trending Today', fontsize=14, fontweight='bold')
plt.xlabel('Number of Videos')
plt.ylabel('Category')
plt.tight_layout()
plt.savefig('plots/category_distribution.png', dpi=300)
plt.close()

# 4. VISUALIZATION 2: ดูความสัมพันธ์ระหว่าง Hours vs Views
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='Hours_Since_Published', y='Views', hue='Category', size='Views_per_Hour', sizes=(40, 400), palette='deep')
plt.title('Views vs Hours Since Published (Size = Views/Hour)', fontsize=14, fontweight='bold')
plt.xlabel('Hours Since Published')
plt.ylabel('Total Views (Log Scale)')
plt.yscale('log')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig('plots/views_vs_hours_scatter.png', dpi=300)
plt.close()

print("📊 สร้างกราฟสรุป insights 2 รูปสำเร็จ! บันทึกไว้ที่โฟลเดอร์ 'plots/' เรียบร้อย")