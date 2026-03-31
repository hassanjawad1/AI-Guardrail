from graph import graph

def save_graph():
    # Generate Mermaid diagram
    mermaid = graph.get_graph().draw_mermaid()

    # Save to file
    with open("graph.mmd", "w") as f:
        f.write(mermaid)

    print("✅ Mermaid graph saved as graph.mmd")


if __name__ == "__main__":
    save_graph()