#!/usr/bin/env python3
import json, sys
import matplotlib.pyplot as plt

def render(geo_path, out_path="assets/maps/geo_overlay.png", title="SCS (simplified EEZ/features)"):
    with open(geo_path, "r", encoding="utf-8") as f:
        gj = json.load(f)
    plt.figure()
    ax = plt.gca()
    for feat in gj.get("features", []):
        g = feat.get("geometry", {}); t = g.get("type")
        if t == "LineString":
            xs = [c[0] for c in g["coordinates"]]
            ys = [c[1] for c in g["coordinates"]]
            ax.plot(xs, ys)
        elif t == "Polygon":
            for ring in g["coordinates"]:
                xs = [c[0] for c in ring]
                ys = [c[1] for c in ring]
                ax.plot(xs, ys)
        elif t == "Point":
            x,y = g["coordinates"]
            ax.scatter([x],[y])
    plt.title(title); plt.xlabel("Longitude"); plt.ylabel("Latitude")
    plt.savefig(out_path, bbox_inches='tight')
    print("Saved", out_path)

if __name__ == "__main__":
    geo = sys.argv[1] if len(sys.argv)>1 else "assets/geo/sample_scs.geojson"
    out = sys.argv[2] if len(sys.argv)>2 else "assets/maps/geo_overlay.png"
    render(geo, out)
