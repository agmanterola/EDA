import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# Variables
# Columns we are interested in. Focusing on retreiving only these columns will use less computing resources
req_cols = ['generated_on', 'display_name', 'load_month', 'dlvd_price']
out_cols = ['generated_on', 'display_name', 'Sep.21', 'Oct.21', 'Nov.21', 'Dec.21', 'Jan.22', 'Feb.22']
month_cols = ['Sep.21', 'Oct.21', 'Nov.21', 'Dec.21', 'Jan.22', 'Feb.22']

# Function that take different date formats of a columns and unify them under same datatype.
# Args:
#   Datetime Column with different datetiem formats to be converted to datetime.
# Returns:
#   A converted datetime column
def date_conv(src):
    return pd.to_datetime(src)


# Function to read a CSVfile and clean it.
# Args:
#   inputfile: raw file to read and clean
# Retruns:
#   data_df: A cleaned and ready to plot dataframe
def read_and_clean(inputfile):
    # Gets the in file to be load into a dataframe
    # data_df = pd.read_csv(inputfile, usecols=req_cols)

    # Having in mind how the dataset look like let's fix it accordignly
    # Header goes in the first line:
    #data_df = pd.read_csv("C:/SpartaTest/RBOB_data_test.csv", header=[0], sep=",")#, index_col=0, usecols=req_cols)
    data_df = pd.read_csv("C:/SpartaTest/RBOB_data_test.csv", usecols=req_cols)
    # Initially keep selected columns so it will use less memory
    #data_df = data_df[['generated_on','display_name','load_month','dlvd_price']]

    # Data Preparation:
    # Only filed to take care of is the datetime of 'generated_on'
    # A method will put all dates in the same format
    data_df['generated_on'] = data_df['generated_on'].apply(date_conv)

    ### Reshaping dataframe from long data to wide data
    data_df = data_df.pivot_table(index=['generated_on', 'display_name'], values='dlvd_price', columns='load_month')
    data_df = data_df.reset_index()
    data_df = data_df[out_cols]

    return data_df

# Outlier removal method implementation
# This method identifies the outliers of the selected columns and returns that column after the removal has been applied.
# Args:
#   df: Dataframe which outliers have to be identified
#   column: name of the column to treat into dataframe
# Retunrs:
#   removed_outliers: Index of data that is considered an Outlier
def outlier_removal(df, column):
    # Get the column of the dataframe to be cleaned
    cleaning_col = df[column]
    # Calculate it's mean and standard deviation
    std = cleaning_col.std()
    mean = cleaning_col.mean()

    # Identify the Outliers and marked (replace) them with NaN values
    cleaning_col = np.where(((cleaning_col < (mean-4*std)) | (cleaning_col > (mean+4*std))), np.NAN, cleaning_col)
    # Calculate the mean without Outliers
    new_mean = np.nanmean(cleaning_col)
    # Replace the mean value in those marked NaN values
    cleaning_col = np.where(np.isnan(cleaning_col), new_mean, cleaning_col)
    return cleaning_col


# Plotting dataset method implementation
# This method takes a dataframe and plots it based on input file structure (it's an ad-hoc plot)
# Args:
#   df: Dataframe which outliers have to be identified
#   stop: Boolean indicating to stop the program execution until closing the plot window
# Retunrs:
#   It doesn't return anything, but the plot will appear on the screen
def plot_data(df,stop=False):
    # Plot data
    plt.plot(df['generated_on'], df['Sep.21'], label="Sep.21")
    plt.plot(df['generated_on'], df['Oct.21'], label="Oct.21")
    plt.plot(df['generated_on'], df['Nov.21'], label="Nov.21")
    plt.plot(df['generated_on'], df['Dec.21'], label="Dec.21")
    plt.plot(df['generated_on'], df['Jan.22'], label="Jan.22")
    plt.plot(df['generated_on'], df['Feb.22'], label="Feb.22")
    plt.legend()
    plt.show(block=stop)


# Boxplotting dataset method implementation
# This method takes a dataframe and tries to get a test of the value dispersion of the columns
# Args:
#   df: Dataframe which outliers have to be identified
#   stop: Boolean indicating to stop the program execution until closing the plot window
# Retunrs:
#   It doesn't return anything, but the plot will appear on the screen
def boxplot_dispersion(df, stop=False, cols=month_cols):
    fig = plt.figure()
    # Figure size
    fig.set_size_inches(8.5, 5)
    df.boxplot(column=cols)
    plt.show(block=stop)



# Main execution
# Read the file and get data prepared
prep_df = read_and_clean("C:/SpartaTest/RBOB_data_test.csv")

# Plot read data
plot_data(prep_df, True)

## Outlier identification and cleaning

# Bloxplot values
boxplot_dispersion(prep_df, True)

# Applying the cleaning strategy to remove outliers
for col in month_cols:
    prep_df[col] = outlier_removal(prep_df, col)

# Bloxplot values of cleaned data
boxplot_dispersion(prep_df, True)

# Plotting cleaned dataset
plot_data(prep_df, True)

# Writing cleaned dataset down to a CSV file
prep_df.to_csv(r'C:\SpartaTest\RBOB_data_clean.csv', columns=out_cols, index=False)

print("End of script")


