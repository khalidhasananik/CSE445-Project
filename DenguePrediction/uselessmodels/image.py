import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

# Load your CSV file
file_path = "dataset/dataset.csv"  # Replace with your CSV file path
df = pd.read_csv(file_path)

# Display only the first few rows (e.g., first 10 rows)
rows_to_display = 10
df_subset = df.head(rows_to_display)

# Split the columns into two groups
group1 = df_subset.iloc[:, :10]  # First 10 columns
group2 = df_subset.iloc[:, 10:20]  # Next 10 columns
group3 = df_subset.iloc[:, 20:30]  # Next 10 columns
group4 = df_subset.iloc[:, 30:40]  # Next 10 columns
group5 = df_subset.iloc[:, 40:]  # Remaining columns

# Function to save a styled table as an image
def save_table_as_image_with_style(dataframe, filename, fixed_width):
    # Create a figure
    fig, ax = plt.subplots(figsize=(fixed_width, rows_to_display * 0.5))
    ax.axis('tight')
    ax.axis('off')

    # Define colors for alternating rows and header
    row_colors = ["#f9f9f9", "#e3f2fd"] * (len(dataframe) // 2 + 1)  # Alternating row colors
    header_color = "#2196f3"  # Blue header
    header_font_color = "white"

    # Add table with styling
    table = ax.table(
        cellText=dataframe.values,
        colLabels=dataframe.columns,
        cellLoc='center',
        loc='center',
    )

    # Apply styles
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.auto_set_column_width(col=list(range(len(dataframe.columns))))  # Adjust column width dynamically
    table.scale(1.2, 1.5)  # Scale the table for better visuals

    # Set header styles
    for col_index in range(len(dataframe.columns)):
        cell = table[(0, col_index)]
        cell.set_facecolor(header_color)
        cell.set_text_props(color=header_font_color, weight="bold")
        cell.set_edgecolor("black")
        cell.set_linewidth(0.8)

    # Set alternating row colors
    for row_index in range(1, len(dataframe.values) + 1):  # Start after header
        for col_index in range(len(dataframe.columns)):
            cell = table[(row_index, col_index)]
            cell.set_facecolor(row_colors[row_index % 2])  # Alternate colors
            cell.set_edgecolor("black")
            cell.set_linewidth(0.5)

    # Save the styled table as an image
    plt.savefig(filename, bbox_inches='tight', dpi=300)
    plt.close(fig)

# Save styled images for both groups
# Calculate the height based on the number of rows to display
fixed_height = rows_to_display * 0.1

save_table_as_image_with_style(group1, "table_group1_styled.png", fixed_width=15)
save_table_as_image_with_style(group2, "table_group2_styled.png", fixed_width=15)
save_table_as_image_with_style(group3, "table_group3_styled.png", fixed_width=15)
save_table_as_image_with_style(group4, "table_group4_styled.png", fixed_width=15)
save_table_as_image_with_style(group5, "table_group5_styled.png", fixed_width=15)

print("Styled images saved as 'table_group1_styled.png' and 'table_group2_styled.png'")
