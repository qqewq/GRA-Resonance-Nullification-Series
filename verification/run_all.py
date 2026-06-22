import subprocess, sys, os
scripts = [
    'fig_resonance_suppression.py',
    'fig_latent_lri.py',
    'toy_latent_resonance.py',
    'chiral_swarm_stability.py'
]
os.makedirs('../figures', exist_ok=True)
for s in scripts:
    print(f'--- Запуск {s} ---')
    res = subprocess.run([sys.executable, s], capture_output=True, text=True)
    if res.returncode == 0:
        print(f'✅ {s}\n{res.stdout}')
    else:
        print(f'❌ {s}\n{res.stderr}')
