import plotly.graph_objs as go

def draw_half_court(fig, court_color='black', court_alpha=1.0, lw=2):
    # Simulate parquet pattern with custom colors
    for i in range(15):
        for j in range(4):
            color = '#D2B48C'
            fig.add_shape(
                type="rect",
                x0=i * 3.33,
                y0=j * 12,
                x1=(i + 1) * 3.33,
                y1=(j + 1) * 12,
                line=dict(color=color),
                fillcolor=color,
                opacity=0.8
            )

    # Draw the hoop
    fig.add_shape(
        type="circle",
        x0=24.25, y0=4.5, x1=25.75, y1=6.0,
        line=dict(color=court_color, width=lw),
        opacity=court_alpha
    )
    
    # Draw the backboard
    fig.add_shape(
        type="rect",
        x0=22, y0=4, x1=28, y1=4.5,
        line=dict(color=court_color, width=lw),
        opacity=court_alpha
    )
    
    # Draw the paint (key)
    fig.add_shape(
        type="rect",
        x0=19, y0=0, x1=31, y1=19,
        line=dict(color=court_color, width=lw),
        opacity=court_alpha
    )
    
    # Draw the free throw circle
    fig.add_shape(
        type="circle",
        x0=19, y0=13, x1=31, y1=25,
        line=dict(color=court_color, width=lw),
        opacity=court_alpha
    )
    
    # Draw the free throw circle inner part (dashed)
    fig.add_shape(
        type="circle",
        x0=19, y0=13, x1=31, y1=25,
        line=dict(color=court_color, width=lw, dash='dash'),
        opacity=court_alpha
    )
    
    # Draw the corner three-point lines
    fig.add_shape(
        type="line",
        x0=3, y0=0, x1=3, y1=14,
        line=dict(color=court_color, width=lw),
        opacity=court_alpha
    )
    fig.add_shape(
        type="line",
        x0=47, y0=0, x1=47, y1=14,
        line=dict(color=court_color, width=lw),
        opacity=court_alpha
    )
    
    # Draw the three-point arc
    fig.add_shape(
        type="path",
        path=f"M 3 14 Q 25 47.5 47 14",
        line=dict(color=court_color, width=lw),
        opacity=court_alpha
    )
    
    # Draw the center court
    fig.add_shape(
        type="circle",
        x0=19, y0=41, x1=31, y1=53,
        line=dict(color=court_color, width=lw),
        opacity=court_alpha
    )
    
    # Draw the center line
    fig.add_shape(
        type="line",
        x0=0, y0=47, x1=50, y1=47,
        line=dict(color=court_color, width=lw),
        opacity=court_alpha
    )

    # Set the aspect ratio and remove axes
    fig.update_layout(
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        showlegend=False,
        plot_bgcolor='white',
        paper_bgcolor='white',
        width=600,
        height=600
    )

def plot_team_basket(liste_equipe,nom_equipe):
    fig = go.Figure()

    # Draw the half-court
    draw_half_court(fig)

    # Define the positions for the players
    positions = {
        "1": (25, 35),    # Point Guard
        "2": (10, 26),    # Shooting Guard
        "3": (37, 10),    # Small Forward
        "4": (15, 13),    # Power Forward
        "5": (33, 17),    # Center
    }

    # Plot each player position with labels and circles
    for pos, (x, y) in positions.items():
        fig.add_trace(go.Scatter(
            x=[x],
            y=[y],
            mode='markers+text',
            marker=dict(
                size=40,
                color='rgba(255, 255, 255, 0.8)',  # Less transparent circle
                line=dict(color='black', width=2)
            ),
            text=[pos],
            textposition="middle center",
            textfont=dict(
                size=16,
                color='black',
                family='Arial, bold'
            ),
            showlegend=False
        ))

    # Label the positions with player names
    labels = {
        "1": liste_equipe[0],
        "2": liste_equipe[1],
        "3": liste_equipe[2],
        "4": liste_equipe[3],
        "5": liste_equipe[4],
    }

    for pos, (x, y) in positions.items():
        fig.add_trace(go.Scatter(
            x=[x],
            y=[y - 4],  # Adjust y position for the label
            mode='text',
            text=[labels[pos]],
            textposition="bottom center",
            textfont=dict(
                size=12,
                color='black',
                family='Arial'
            ),
            showlegend=False
        ))
    fig.update_layout(
    title = f"Line up de l'équipe {nom_equipe}"
    )
    return fig