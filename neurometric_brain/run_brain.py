from neurometric.brain import RealityInputs, score_all

if __name__ == "__main__":
    print("--- Brain Simulation Start ---\n")
    
    x = RealityInputs(
        L_low=0.8, L_mid=0.9, L_high=1.0, S=0.8,
        coping=0.2, rescue=0.1, reversibility=0.1, control=0.2,
        responsibility=0.9, social_eval=0.9, goal_blocked=0.4,
        loss_already_happened=1.0
    )
    
    results = score_all(x)
    
    print(f"{'EMOTION':>12}  {'SCORE':>5}  {'BAND':>7}")
    print("-" * 35)
    for r in results[:10]:
        print(f"{r.name:>12}  {r.score_0_100:>5.1f}  {r.band:>7}")
