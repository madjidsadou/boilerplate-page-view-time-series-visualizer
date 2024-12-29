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
df = df.drop(df[df['value'] < df['value'].quantile(0.025)].index)
df = df.drop(df[df['value'] > df['value'].quantile(0.975)].index)


def draw_line_plot():
    # Ensure the index is in datetime format
    df.index = pd.to_datetime(df.index)

    # Create a figure and axis
    fig, ax = plt.subplots(figsize=(20, 6))

    # Plot 'value' over 'date'
    ax.plot(df.index, df['value'], color='red')

    # Label the axes
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')
    ax.set_title('Daily Forum Page Views')

    # Set the x-axis locator to show every month
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=6))  # 6-month interval

    # Set the lower limit of the x-axis to the desired start date
    start_date = pd.to_datetime('2016-05')  # Set your desired start date here
    ax.set_xlim(left=start_date)  # Set the lower limit to the start_date

    # Set the date format for the x-axis
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))  # Custom date format (Year-Month)

    # Explicitly set the x-axis as a date axis
    ax.xaxis_date()

    # Save image and return the figure (don't change this part)
    fig.savefig('line_plot.png')
    return fig


def draw_bar_plot():
    # Create copy of the data to avoid modifications to original
    df_bar = df.copy()
    
    # Add month and year columns
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.strftime('%B')  # Full month name
    
    # Calculate the mean page views for each year-month combination
    df_bar = df_bar.groupby(['year', 'month'])['value'].mean().reset_index()
    
    # Ensure months are in correct order
    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 
                  'July', 'August', 'September', 'October', 'November', 'December']
    df_bar['month'] = pd.Categorical(df_bar['month'], categories=month_order, ordered=True)
    
    # Sort by year and month
    df_bar = df_bar.sort_values(['year', 'month'])
    
    # Create the plot
    fig, ax = plt.subplots(figsize=(7, 6))
    
    # Create the bar plot
    sns.barplot(data=df_bar, 
                x='year', 
                y='value', 
                hue='month',
                palette='Set2',
                ax=ax)
    
    # Customize the plot
    ax.set_xlabel('Years')
    ax.set_ylabel('Average Page Views')
    
    # Rotate x-axis labels if needed
    plt.xticks(rotation=0)
    
    # Adjust legend position and style
    plt.legend(title='Months',
              bbox_to_anchor=(1.05, 1),
              loc='upper left',
              borderaxespad=0.)
    
    # Adjust layout to prevent label cutoff
    plt.tight_layout()
    
    # Save the plot
    fig.savefig('bar_plot.png',
                dpi=300,
                bbox_inches='tight')
    
    return fig

    
def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)





    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
