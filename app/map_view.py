import folium


def create_map(user_location, spot_locations, best_spot_id, ranking_data):

    m = folium.Map(
        location=user_location,
        zoom_start=14
    )

    # User marker
    folium.Marker(
        location=user_location,
        popup="Your Location",
        tooltip="Your Location",
        icon=folium.Icon(color="blue", icon="user")
    ).add_to(m)


    # Spot markers
    for spot_id, location in spot_locations.items():

        color = "green"
        status = "Viewing Spot"

        if spot_id == best_spot_id:
            color = "red"
            status = "⭐ Recommended Spot"


        # Find crowd information
        spot_data = next(
            (
                item for item in ranking_data
                if item["spot_id"] == spot_id
            ),
            None
        )


        crowd_info = ""

        if spot_data:
            crowd_info = f"""
            <br>
            Crowd Level: {spot_data['crowd_level']}<br>
            People: {spot_data['head_count']}
            """


        popup_text = f"""
        <b>{spot_id.replace("_", " ").title()}</b><br>
        {status}
        {crowd_info}
        """


        folium.Marker(
            location=[
                location["latitude"],
                location["longitude"]
            ],
            popup=popup_text,
            tooltip=spot_id.replace("_", " ").title(),
            icon=folium.Icon(color=color)
        ).add_to(m)
    
        # Route line to recommended spot
    best_location = spot_locations[best_spot_id]

    folium.PolyLine(
        locations=[
            user_location,
            [
                best_location["latitude"],
                best_location["longitude"]
            ]
        ],
        weight=4,
        tooltip="Recommended Route"
    ).add_to(m)


    # Map Legend
    legend_html = """
    <div style="
    position: fixed;
    bottom: 50px;
    left: 50px;
    width: 220px;
    background-color: white;
    border: 2px solid grey;
    z-index: 9999;
    padding: 10px;
    font-size: 14px;
    color: black;
    ">
    <b>Map Legend</b><br>
    🔵 Your Location<br>
    🟢 Viewing Spots<br>
    🔴 Recommended Spot
    </div>
    """


    m.get_root().html.add_child(
        folium.Element(legend_html)
    )


    return m