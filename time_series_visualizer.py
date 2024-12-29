import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
from matplotlib.ticker import MaxNLocator
import matplotlib.dates as mdates

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv',date_parser = True, )
df.set_index('date', inplace=True)
# Clean data
df = df[(df['value'] > df['value'].quantile(0.025)) & (df['value'] < df['value'].quantile(0.975))]


def draw_line_plot():
    # Ensure the index is in datetime format
    df.index = pd.to_datetime(df.index)

    # Create the plot
    fig, ax = plt.subplots(figsize=(20, 6))
    ax.plot(df.index, df['value'], color='red')

    # Set title and labels
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')  # Fix title
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')

    # Format x-axis
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=6))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))

    # Save and return figure
    fig.savefig('line_plot.png')
    return fig


def draw_bar_plot():
    # Create a copy of the data
    df_bar = df.copy()

    # Add year and month columns
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month

    # Group by year and month to calculate the mean
    df_bar = df_bar.groupby(['year', 'month'])['value'].mean().reset_index()

    # Map month numbers to their names
    month_order = ['January', 'February', 'March', 'April', 'May', 'June',
                   'July', 'August', 'September', 'October', 'November', 'December']
    df_bar['month'] = df_bar['month'].apply(lambda x: month_order[x-1])

    # Ensure months are ordered correctly
    df_bar['month'] = pd.Categorical(df_bar['month'], categories=month_order, ordered=True)
    df_bar = df_bar[df_bar['value'].notna()]

    # Plot the data
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=df_bar, x='year', y='value', hue='month', palette='Set2', ax=ax)

    # Set labels
    ax.set_xlabel('Years')
    ax.set_ylabel('Average Page Views')

    # Adjust legend
    plt.legend(title='Months', bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)

    # Adjust layout to prevent cutoff
    plt.tight_layout()

    # Save and return the figure
    fig.savefig('bar_plot.png')
    return fig
    
def draw_box_plot():
    # Prepare data
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = df_box['date'].dt.year
    df_box['month'] = df_box['date'].dt.strftime('%b')

    # Draw box plots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 6))

    # Year-wise Box Plot
    sns.boxplot(data=df_box, x="year", y="value", ax=ax1, palette='husl')
    ax1.set_title("Year-wise Box Plot (Trend)")
    ax1.set_xlabel("Year")
    ax1.set_ylabel("Page Views")  # Fix the ylabel

    # Month-wise Box Plot
    month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                   "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    sns.boxplot(data=df_box, x="month", y="value", order=month_order, ax=ax2, palette='husl')
    ax2.set_title("Month-wise Box Plot (Seasonality)")
    ax2.set_xlabel("Month")
    ax2.set_ylabel("Page Views")  # Fix the ylabel

    # Adjust layout
    plt.tight_layout()

    # Save and return figure
    fig.savefig('box_plot.png')
    return fig
