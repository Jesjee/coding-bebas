
x = radius * np.cos(sudut)
y = radius * np.sin(sudut)

# Warna emas kekuningan dengan gradasi
warna = np.linspace(0.1, 1, jumlah_biji)
warna_rgb = plt.cm.inferno(warna)  # bisa diganti 'autumn', 'plasma', dll

# Buat plot
fig, ax = plt.subplots(figsize=(8, 8), facecolor='black')
ax.set_facecolor("black")
ax.scatter(x, y, c=warna_rgb, s=8, edgecolors='none')
ax.axis("off")
plt.tight_layout()
plt.show()
