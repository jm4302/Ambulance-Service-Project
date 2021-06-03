# Ambulance-Service-Project
## Purpose
With great pride and commitment, I have served the Whitestone Community Ambulance Service for nearly a decade as a Dispatcher, Ambulance Driver, Grant Writer and currently hold the position of Vice President of the organization. Throughout this timespan, I have witnessed the organization flourish with great operational success providing a free emergency ambulance to the residents of a suburban NYC town within Queens County. The daily operations of the service have always been held to the highest standard as nearly 100% of all emergency calls have been tended to by our uncompensated volunteers. Over the past year and a half however, sudden operational changes along with the COVID-19 pandemic threatened the longevity of the service and swift action was necessary to save it. The purpose of this project was to identify the points of failure based on monthly and yearly call volumes and address the long-term solutions through forecasting models with respect to hourly call volume patterns. Disseminating the call volume in such a detailed fashion has yielded insight into our best periods of performance, the failures, and effective approaches to staffing the ambulance have emerged from it. This notebook has also been adopted as a tool to drive daily operations and monitor the monthly performance of the service. Through these efforts, we have been able to continue our mission of saving lives for free.  

### Note to Reader
The contents of this project notebook are specifically tailored to extract from the file `Call_Data_Master_2020.csv` which contains a collection of dates and times that are later converted into `datetime` format. The code also separates the data into four distinct categories which will be explained in the notebook description section. Running this notebook on other collections of data or a time series is possible if the time series conversion step is removed and adjustments to the number of features you are working with is adjusted accordingly.

## Summary of Contributed Files  
The two main proponents of this project pertain to `Call_Data_Master_2020.csv` and `Ambulance_Service_Model.ipynb` and correspond to the primary data file and main notebook respectively. To run the notebook and read the .csv file, simply use `Python 3.7.3` or newer and make sure `tensorflow`, `fbprophet`, `statsmodels`, `pmdarima` and `sklearn` are installed in your distribution of Python. If the code does not run please check which packages are missing from the list of imported packages in the project notebook. For convenience `Ambulance_Service_Model.html` is provided as a viewable desktop browser copy of the notebook.

Attachments `WVAS_Call_Volume_Study_Letters.PDF` and `WVAS_New_Operations_Order.PDF` contained in the folder `Project_Documents` are included to explain the need for this study, document the project progress and outline the operational changes made as a result of the exploratory analysis and data modeling performed. While the code is of value, it's only effective as its impact and these documents showcase that matter exceptionally. Please refer to them for a broader understanding of the project beyond the Python code. The Conclusion section at the end of this readme.md also provides a synopsis of the solutions and outcomes as well.     

## Description of Notebook
The notebook `Ambulance_Service_Model.ipynb` can be broken down into three sections: Data Pre-Processing, Exploratory Analysis and Modeling. Each part will contain a brief walkthrough of what was done.  
***
## Data Pre-Processing
Upon running the notebook, `Call_Data_Master_2020.csv` is read from its file location into Python as the dataframe `df`. This csv file contains over 2,300 patient care reports that were filled out at the scene of an emergency call from 2017 - 2020. The information ascertained from these reports was used to place the calls into one of four call categories:

1. Total Phone Demand - All phone calls made to ambulance station

    `df_Phone = df[df['1000 Line'] == 'Yes']`
    
    
2. Met Phone Demand - Phone calls the ambulance responded to

    `df_Phone_Met = df[(df['1000 Line'] == 'Yes') & (df['Disposition'] != 'Unmet Demand')]`
    
    
3. Unmet Phone Demand - Phone calls the ambulance did not respond to

    `df_Phone_Unmet = df[(df['1000 Line'] == 'Yes') & (df['Disposition'] == 'Unmet Demand')]`    
    
    
4. Radio Activity - Optional calls the ambulance responded to through the 911 network

    `df_Radio = df[df['1000 Line'] == 'No']`    

**Note:** Total Phone Demand is a sum of Met and Unmet Phone Demand

Applying this selection criteria came with ease due to the forethought put into the structure of the dataset. The dataframe column `1000 Line` was used to determine whether a call was made directly to the ambulance station and was marked as 'Yes' or 'No' while `Disposition` refers to the outcome of the call. If the disposition of Phone Demand is 'Unmet Demand' then call was missed otherwise it was met by the ambulance crew. By doing this, the call categories are separated into four separate dataframes for convenient accessibility.       

Date and time entries for each call were converted into `datetime` format so that the hour from the call time, month number and name, and the year could be found and appended to the dataframe `df`. These additional columns of event information are continuously used throughout the notebook to iterate through the structured dataset. All Yearly and Monthly Call volume variables are defined in this section and populated with a `for loop` over the variable `year_range_all`. This variable creates a list of all the unique years within the dataframe. In this case, the code iterates through four calendar years chronologically for each call volume category. If a user wants to look at a specific combination of calendar years they can specify the list manually and assign it to `year_range_all`. The Monthly and Yearly call volumes were calculated for all four of the call volume categories in preparation for exploratory analysis. 
***
## Exploratory Analysis
The exploratory analysis section was used to quantify the features and remove any collinear variables. All figures contain qualitative descriptions with respect to the call volume categories as a function of time, please reference the notebook for the details. To summarize, exploratory analysis revealed the following:

    • Phone demand is the driving force of the ambulance service
    • Phone demand and Radio Activity are independent features  
    • 2017 and 2018 were great examples of operational success
    • September 2018 was the initial indicator of a decline in the percentage of completed phone demand
    • 2019 saw Total Phone Demand and Radio Activity decline along with a continued drop in completed phone demand
    • JAN 2020 - MAR 2020 saw the worst consecutive monthly performance in call volume due to the COVID-19 Pandemic
    • APR 2020 a third party ambulance service was introduced to help handle Unmet Phone Demand
    • The last quarter of 2020 saw monthly call volume outperform what it achieved a year ago and continues to recover
    
**Note:** The last two bullets were added upon completion of the study

The data was visualized with line graphs, bar charts, boxplots and pie charts to highlight the comparisons between call volume categories over time. To understand the magnitude of calls that have been completed by the service over the past 4 years, an aggregate bar chart, boxplot and pie chart have been provided to highlight the context. The project notebook contains an intricate breakdown of these figures by year as a supplement to the cumulative totals.  

![operational_summary](https://user-images.githubusercontent.com/25239215/114750760-54aced00-9d22-11eb-9fe0-667d0d589c77.png)

The primary feature for modeling was identified as Total Phone Demand and includes both met and unmet calls. While Yearly Call Volume provided a macroscopic perspective on operations and Monthly call volume revealed the periods of success/failure over time, no recurrent pattern or seasonal trend could be found. To generate a model, a recurrent pattern was needed so a creative solution was devised to find it.
***
### Daily and Hourly Call Volume Pre-Processing
To resample the data in daily and hourly call volume configurations, the hour of each time was reconfigured as a nested dictionary containing two elements. The key accesses the year and the value accesses all of the data pertaining to a specified day of week. Dictionaries `Phone_dict`, `Phone_Met_dict` and `Radio_dict` were created which refer to the call categories Total Phone Demand, Met Phone Demand and Radio Activity respectively. This custom approach enumerated the indicies of the call categories by year, and then repeated the process by enumerating the indicies of the days of the week for each year. The entire process resulted in a nested dictionary containing lists of the hours of each call separated by the days of the week. The next section explains the structure of the dictionaries in further detail below.     
***
### Elements of the nested dictionaries
Among every nested dictionary created, the first element can range between 0 and 4, returning information for any year between 2017 and 2020, respectively. The second element on the other hand can receive any value between 0 and 6 which corresponds to the days of the week, Sunday through Saturday.

**Consider the following examples for clarity:**

**Daily Call Volume:**

`Phone_dict[0][0]`, will return a list for every emergency phone call received on a Sunday in 2017

`Phone_Met_dict[1][3]` will return a list for every met emergency phone call received on a Wednesday in 2018

`Phone_Radio_dict[3][6]` will return a list for every response to radio calls received on a Saturday in 2020


These dictionaries were then utilized to create lists of the daily call volumes for each year. The element value can range between 0 and 4 and the length of the selected list will always be 7.

**Hourly Call Volume:**

`Hours_list_Phone_yearly[0]` will return the daily call volume of every emergency phone call for each day of the week in 2017

`Hours_list_Phone_Met_yearly[1]` will return the daily call volume of every met emergency phone call for each day of the week in 2018

`Hours_list_Radio_yearly[2]` will return the daily radio activity responses for each day of the week in 2019


By taking the sum of the daily call volume dictionaries, the cumulative daily call volumes of all years were made. These variables include: `Count_Phone`, `Count_Phone_Met` and `Count_Radio`

**Note:** To understand how these dictionaries were appended, please reference the project notebook code for details
***
## Exploratory Analysis Cont'd (Daily and Hourly Call Volume) 

In the previous section, the initial exploratory analysis revelated that Total Phone Demand was the primary feature to base a model on. To further confirm this, the weekly and daily trends stemming from daily and hourly call volumes were made. The plots show a comparison of the desired predictor against the other call volume categories. We will see how the weekly Total Phone Demand trend becomes a relevant component later on in the modeling section. Referring back to the original call categories, three dictionaries were created which include Total Phone Demand, Met Phone Demand and Radio Activity. Taking advantage of `Count_Phone`, `Count_Phone_Met` and `Count_Radio`, the daily call volumes were plotted and displayed the cumulative and yearly totals over an aggregate week. 

![daily_cv](https://user-images.githubusercontent.com/25239215/114750829-6a221700-9d22-11eb-94b7-4c4114df9692.png)

The totals are displayed according to the legend. Note that the values shown above the blue-green bars are based in `Count_Phone` which represents Total Phone Demand (the sum of met and unmet phone demand). Unmet Phone Demand shown in green, is a superposition of Total Phone Demand on top of the Met Phone Demand bar. The reveal or "difference" where Total Phone Demand surpasses Met Phone Demand provides a visual as to what portion of the calls were unmet over time per day. By constructing an aggregate total of the daily call volumes, a weekly pattern has emerged for each call category. Consult the project notebook for the specific breakdowns of all call category totals for aggregate and yearly totals.
***   
Moving to hourly call volume, the restructured data saved in the dictionaries `Phone_dict`, `Phone_Met_dict` and `Radio_dict` gave rise to histograms for each call category. Each day of the week is a subplot and contains 24 individual bins for each hour of the day. The counts are displayed as a function of time, labeled at 6 hour intervals. Below are the aggregate histograms for each call category. The project notebook also contains the same collection of data broken down by year as well. 

![met_unmet_phone](https://user-images.githubusercontent.com/25239215/114750927-8920a900-9d22-11eb-80b5-bc8338b3c850.png)

![radio](https://user-images.githubusercontent.com/25239215/114750960-9047b700-9d22-11eb-9fb2-9836e63e509a.png)

The two resulting figures are a decomposition of the daily call volume totals from the previous section. Hourly call volume adds another layer of perspective and the common times for each call category are ascertained. The spacing between the peak demand times for Phone Demand remains consistent at 6 hour intervals on average. 
***
![total_phone](https://user-images.githubusercontent.com/25239215/114750988-9b9ae280-9d22-11eb-8915-d07c8dd25ca0.png)

A recurrent pattern manifests among phone demand. For a clearer look at the hourly trend, the Met and Unmet partitions have been removed to reflect Total Phone Demand. While the daily trend has emerged visually, more work needs to be done to quantify the pattern. 

**Note:** All models were created utilizing the weekly aggregate collection of Total Phone Demand Hourly Call Volume 
    
<p align="center">
  <img src="https://user-images.githubusercontent.com/25239215/114751039-a9e8fe80-9d22-11eb-81d0-207f731e1baa.png">
</p>

An outline of the Total Phone Demand histogram was taken and converted into a line graph to highlight the primary and secondary peaks of demand shown in red and green respectively. A threshold was set to filter out call frequencies that were too far from the max daily call volume. A second condition was set to find the secondary peak relative to the proximity of the primary peak - see notebook for details. 

<p align="center">
  <img src="https://user-images.githubusercontent.com/25239215/114751133-bff6bf00-9d22-11eb-8c59-3bf42c139aff.PNG">
</p>

The table above summarizes the windows of time between the two defined peaks for phone demand based on thresholding and peak separation. Each peak is defined with a time and frequency. Creating a manual method for peak selection establishes a reference to the true busiest times for each day of the week. Knowing the true weekly and daily trends provided a good basis of how well the models are generalizing to the data. The rise and fall of demand around a peak will be referred to as a wave of demand. In the next section, these concepts are drawn upon more. 
***
## Modeling

### ARIMA Forecasting
Baseline predictions for time series forecasting were made using an ARIMA model. `arimaMaker.py` is a OOP Python script that contains the class `arimaMaker` which is capable of fitting and displaying an Arima model with the function `ARIMA` imported from `statsmodels.tsa.arima_model.ARIMA`. The constructed class takes in five parameters:

`arimaMaker`(num_prediction_days, p, d, q, data)

The parameter `num_prediction_days` specifies how many days will be forecasted on and the appropriate train-test split is performed on the data. If the parameter is less than or equal to 3, the model will forecast the end of the week. Setting `num_prediction_days` to greater than 3 forecasts the beginning of the week. This was done to highlight different variations of the train-test split but the order can just as easily be reversed. The order of the model for the autoregressive, differences, and moving average components are (p,d,q) respectively. Finally, the input is specified by the parameter `data` which is set equal to the data desired to be modeled.

The script `arimaMaker.py` contains three methods related to creating and displaying the model. `arimaMaker.train()` fits the model and makes a forecast, `arimaMaker.plotter()` shows the stationarized data, residual errors KDE, and autocorrelation and partial autocorrelation plots for the model. The results are then plotted which compares the test data to the predictions over the span of the prediction days. `arimaMaker.stats()` provides the MSE, RMSE, MAPE and R&sup2; value of the prediction relative to the test data. Upon instantiating the class `arimaMaker` to the object `Arima`, these three methods can be run instantaneously with the function call `Arima.train_and_display()` and are executed in the aforementioned order.   
***
Provided below are the results of the two train-test split attempts utilizing Holt's Linear Method - ARIMA(0,2,2) 

**Case 1** - Trained On: 57.1 % Tested On: 42.9 %

<p align="center">
  <img src="https://user-images.githubusercontent.com/25239215/114751198-d69d1600-9d22-11eb-8b36-7e1b3cbdb7fb.png">
</p>

![Arima_1](https://user-images.githubusercontent.com/25239215/114751221-ddc42400-9d22-11eb-8c2c-1b214c315c6c.png)

    Test MSE: 1.824
    Test RSME: 1.351
    Test MAPE: 1.061
    Test R²: 0.859    
***
**Case 2** - Trained On: 42.9 % Tested On: 57.1 %

<p align="center">
  <img src="https://user-images.githubusercontent.com/25239215/114751259-eb79a980-9d22-11eb-994b-628448a8e5c4.png">
</p>

![Arima_2](https://user-images.githubusercontent.com/25239215/114751272-f16f8a80-9d22-11eb-8989-b8a6d2621ff3.png)

    Test MSE: 2.432
    Test RSME: 1.560
    Test MAPE: 1.256
    Test R²: 0.864

    • Linear Exponential Smoothing performed well on both out-of-time cross validation sets.
    • This model implements two orders of differencing and 2 time lags for the error terms for the MA component.
    • Correlation coefficient of the predictions relative to the test data was greater than 0.85
    • Almost all of the lags in the ACF and PACF fall below or near the significance level
    • For both cases the predictions assume the general shape of the test data
***
### Gaussian Kernel Density Estimate
The purpose of the Gaussian KDE function was to estimate the shape of the input data and identify the primary and secondary peaks of demand. Applying the Gaussian function adequately smoothened the original phone demand data while retaining pertinent information with respect to time. The local maxima with the two greatest densities were found for each estimated probability density function and labels for the primary and secondary peaks were made accordingly.

![ecdf_](https://user-images.githubusercontent.com/25239215/114751325-00563d00-9d23-11eb-9095-690f211fe482.png)

By generalizing the Total Phone Demand data, we see the profile of the density distribution varied by the day of the week. The primary peak typically manifests before noon while the secondary peak occurs after 3pm. The variations of peak times (primary and secondary) and the time difference between them (Time Window) are summarized as a table.
***
The Thresholding Method was used as a baseline for the true results to see how well the Gaussian KDE estimates the shape of the data. The table below highlights the differences in results between thresholding the raw data vs. smoothening the data and finding the local maxima.

<p align="center">
  <img src="https://user-images.githubusercontent.com/25239215/114751338-09dfa500-9d23-11eb-873e-51245f2b0e7f.PNG">
</p>

• The local maxima extracted from the KDE models identified the peak times for Friday, Saturday and Sunday identically to the Thresholding Method. The peaks for these graphs were clearly defined for the local maxima to be found accurately.

• The primary and secondary times for Wednesday and Thursday were both 1 hour off from the expected times. When comparing the primary peaks from raw data to the KDE plots for these days however, the discrepancy is reasonable due to the proximity of the primary and secondary peaks. Based on the lambda value, the general behavior of the smoothing function, the peaks were generalized and shifted over by 1 hour. The secondary time for Tuesday faced the same issue but the secondary time was marked 2 hours earlier than the expected time.

By smoothening the data with a Gaussian function, we see how the raw data transforms into waves of demand which are defined by their local maxima. Through close observation, there are three waves of demand that exist daily with varying likelihoods. These waves typically manifest mid to late morning, early evening and midnight in descending probability.   
***
Taking the Gaussian KDE of all the days in the aggregate week yields a more generalized distribution than the previous estimation:

<p align="center">
  <img src="https://user-images.githubusercontent.com/25239215/114751383-18c65780-9d23-11eb-8a83-14acbdb66a70.png">
</p>

The two greatest local maxima correspond to the primary peak at 1130 hrs and the secondary peak at 1730 hrs respectively. A third peak makes it way slightly past midnight. Making an estimation in this way is comparable to taking the average of all of the peaks in the aggregreate week. 

Up until this point, the weekly trend has been ascertained via exploratory analysis and a daily trend has been established through preliminary modeling. The next section will explore a model which integrates these components to create a more comprehensive model. 
***
### Prophet Forecasting
Facebook's prophet model was used to forecast the data based on an additive model fitting non-linear trends based on seasonal components. The model was trained on the first half of the week (Sunday-Wednesday) and used to make predictions on the second half of the week (Thursday-Saturday) 

<p align="center">
  <img src="https://user-images.githubusercontent.com/25239215/114751441-27ad0a00-9d23-11eb-9d8c-0ad2827ae1de.PNG">
</p>

The resulting forecast captures the daily and weekly trend accordingly along with uncertainty intervals. We see that the prophet model emulates a recurrent daily trend which drifts in amplitude to reflect the fluctuations of the weekly trend. 
***
The forecast components resemble trends established in the earlier part of this study. This observation brings the results of the Prophet Model full circle because the components can be validated by the preceding exploratory analysis and preliminary modeling.  

<p align="center">
  <img src="https://user-images.githubusercontent.com/25239215/114751477-2f6cae80-9d23-11eb-944d-0e9d5379cdb2.PNG">
</p>


Starting with the weekly trend, the pattern emulates the changes in aggregate daily call volume of Total Phone Demand. Note the slope between two points (days) is the change in call volume between the start and end of one calendar day. Reference the figure at the beginning of the Exploratory Analysis Cont'd section to visualize the similarity. 

Comparatively, the Prophet model daily trend and the generalized Gaussian KDE are both capable of accurately representing the desired points of interest. According to the table below, both approaches locate the primary and secondary peak times to be at 1130 and 1730 hrs respectively. Where they differ however, is in their shape. The Prophet model addresses the discontinuity transition between days. Notably the amplitude maintains the same height at the beginning and end of the 24 hour cycle; the Gaussian KDE fails to do this. 
***
Another area where the kernel density estimate suffers is generalizing the daily trend. When considering the waves of demand, the transition between each wave is defined by an inflection point. The slope at any instance represents the rise or fall in calls over a period of time. This correlates to a surge in demand leading up to peak times or lay periods of demand during off-peak times. The Prophet model exhibits steeper slopes at the points of inflection which is a better representation of the changes in demand over a 24 hour period. Compared to the Gaussian KDE approach, this model provides more robust results since the daily trend highlights each wave of demand with more distinction.

<p align="center">
  <img src="https://user-images.githubusercontent.com/25239215/114751516-3dbaca80-9d23-11eb-86e5-87efdadfc317.PNG">
</p>

Both methods were able to estimate the Peak Phone Demand Times within reason and maintained the expected Time Window relative to the Thresholding Method. The 30 minute time difference in peak times relative to the baseline is negligible because the average times were rounded to the nearest hour or half hour for simplicity.   
***
## Conclusion - (Solutions and Impact)

### Revised Staffing Approaches
Given the models generated in this call volume study, we are now able to predict the likelihood of an emergency call occurring on any day of the week at a given time. Staffing approaches have been adjusted to achieve weekly autonomy while covering the largest amount of demand possible. Provided that the minimum monthly requirement for the service is 24-hours per month, crews would previously serve two 12 hour shifts per month from 6pm - 6am. Reflecting on the call history however, we know that this is not optimal as the likelihood for phone demand drops past midnight until the early morning. By removing the second half of the 12 hour shift, more opportunities have been created to staff during the times when our services are requested most. In an ideal scenario, staffing a crew weekly for 6 hours on the same day covers the optimal window of demand for that day of the week indefinitely. 

### Increased Public Exposure 
When a crew is on shift and not responding to phone demand, they are actively listening to the 911 radio system. Our staff responds to Radio Activity emergencies exclusively within our zip code. Whether the call turns out to be a run (no patient contact) or a worker (patient contact/transport), public exposure of our service has increased because there are more days with assigned shifts per month. As we continue to service new members of our community, awareness of our organization has spread and our contributor base for donations has grown. By adhering to this model, the likelihood of receiving an emergency call is greater due to our expanded community outreach - and we'll be ready to act when it happens.

Reducing shift durations from 12 to 8 or 6 hours has also improved the quality of work experience on the ambulance for crews on multiple levels. Shorter work hours by default are less physically taxing and allow for greater productivity during shifts. As a result, crews have responded to more calls per month because the second half of a 12 hour shift is no longer expended on off-peak hours. These extra 6 hours and energy are recycled during on-peak hours the following week. Implementing this conservation of time, energy and resources has been key to saving more lives. To cover each day of the week with the staffing patterns devised, a minimum of 7 EMT (Emergency Medical Technician) and MVO (Motor Vehicle Operator) pairs are necessary. 

### Mutual Aid 
Dispatchers are present to answer incoming emergency calls at our station 24 hours 7 days a week. In the event that a call is received, and a duty crew is unavailable, the dispatcher will contact a 3rd party ambulance service to handle the excess demand. Incorporating this option adds another level of autonomy for the service. In previous circumstances, a dispatcher would contact the officer in charge for a solution which caused delays in providing optimal patient care. This delay is no longer existent because there are an array of options to pursue if the call cannot be handled in-house. The new system has also enabled our organization to aid callers that we were unable to help in the past. Occasional requests for non-emergency transport or emergencies outside of the operating territory are now capable of being relayed to a 3rd party service by our dispatchers. These additional calls are now an extension of helping those who were incapable of being serviced by our organization in the past.

### Recruitment
Understanding the staffing patterns to sustain phone demand responses on a basal level has been achieved. Moving forward, we are expanding recruitment efforts to build up the membership base for dispatchers, MVOs and EMTs (listed in increasing order of skill/certification requirements). 

Currently, every new member sworn in is trained to serve as a dispatcher. By meeting the minimum hourly requirement for service and completing the preliminary training certifications, members are eligible to receive ambulance skills and driver training to be cleared as an MVO. Provided an MVO is in good standing, they have earned the privilege of a voucher to attend an EMT class for free. Over time, members have cycled through the ranks in this way which have provided aspects of retention for members.  

A new approach has also been added to expedite the application process. Depending on an applicant's experience, or long-term goals to pursue a career in EMS, medicine or healthcare, they may be encouraged to complete all of the training certifications prior to being sworn in. Applying this "fast-track" for applicants has allowed new members to receive training virtually the next day prior to being inducted. Including an accelerated path to the ambulance for highly motivated prospective members has allowed the training officer to clear new members for ambulance duty in as short as a month - a feat only achieved until now. In this way, we can cover the prioritized optimal windows of demand and then branch out from the peak times based on staff availability and preferences.             

**Using this information, the operational and staffing changes applied yielded a resurgence in call volume and the percentage of completed calls have returned to an acceptable level.** 

### Call Volume Recovery
The figure below presents a monthly timeline of each call category over the past four years. Operations were evidently stable for the 2017 and 2018 calendar years. Over time we see the decline in performance with respect to phone demand and radio activity, followed by the recovery due to this study. Each year is signified by a dotted black line. **2018-01** for example notes the start of the year but reports the cumulative total of December of 2017. This lag stems from each tick mark denoting the beginning of each labeled month. The cumulative total for January 2018, therefore, is reported one time point to the right because January has concluded and all of the daily occurrences are taken into account. 

<p align="center">
  <img src="https://user-images.githubusercontent.com/25239215/114751555-49a68c80-9d23-11eb-8a42-1fe81ad86445.png">
</p>

Ultimately past operational and leadership changes in September of 2018 led to the crash and demise of the service between June 2019 and March 2020. In some cases, the quantity of unmet phone demand surpassed the totals that were being met (notably September of 2019 and March of 2020). Concurrently, this struggle perpetuated as responses to phone demand and radio activity per month were dwindling. 

The dotted red line signifies the instantiation of the new staffing approaches, 3rd party mutual aid and additions to the staffing roster. These changes were deployed in early April but took full effect the following month. As the members of their service regained their bearings from the initial shock of the COVID-19 pandemic, the recovery phase began. Acquiring the proper PPE has enabled our ambulance staff to resume responding to emergencies while safely protecting themselves and those they serve.

Officers of the service have also re-instated the value of listening and responding to radio activity by explaining to ambulance staff of the important relation between public exposure and incoming phone demand. A radio guide has also been created which includes a summary of how to use radio scanners, a list of radio 10-codes and a map of the neighborhood with all relevant boundaries and landmarks - see `WVAS_New_Operations_Order.PDF` for more detail. The encouragement to save as many lives as possible has lifted the morale of members and the numbers pertaining to call volume reflect that. 

Between **MAY 2020** and **OCT 2020**, substantial improvements to call volume have been observed. Met Phone demand is currently comparable to early 2019 totals at approximately 20 calls per month. Unmet Phone demand has been curtailed significantly and has not exceeded more than 2 missed calls in a month since the operational changes were implemented. June 2020 was the first month of the year where all demand was met. Radio Activity is back to performing as well as it had post-COVID and in 2019.

Between **NOV 2020** and **DEC 2020**, Radio activity has been the greatest it ever has been all year. December saw 50 responses to Radio emergencies, the highest total since **JAN 2019**. For two consecutive months in a row, all Phone Demand was met.
***
From  **JAN 2017 - AUG 2018**, 95% of all phone demand was met on average. This span of time portrays the high standard that the service was always held to. Phone Demand Percent Completion Rate defines this percentage as the amount of phone demand that was met relative to Total Phone Demand.

<p align="center">
  <img src="https://user-images.githubusercontent.com/25239215/114751592-56c37b80-9d23-11eb-8254-d590e605b6d1.png">
</p>

Here we see the monthly operational performance of in-house responses with respect to all phone demand received. Three periods of time define the events that transpired post-decline of the service. 

**SEPT 2018 - MAY 2019:** Operational change takes place. Percent Call Completion Rate never reaches 100% again but about 90% of the calls are met on average.

**JUN 2019 - MAR 2020:** Largest period of instability due to mismanagement of the service. Call completion rate hits an all-time low on three different occasions. **JUN 2019** 52.9%, **OCT 2019** 42.9%, **MAR 2020** 28.6%. Despite two intermittent instances of potential recovery, immediate action was needed in midst of the COVID-19 pandemic.  

**APR 2020 - Present:** Phone Demand Percent Completion rate has been restored to 90%. A milestone has been achieved as call volume has not been met at this rate of completion since May of the following year. 
***
The final figure is an alternative way to compare Total Phone demand and Met Phone demand. When 100% of phone demand is met the two lines overlap yielding an overlay between the solid blue line and yellow dotted line.

<p align="center">
  <img src="https://user-images.githubusercontent.com/25239215/114751609-5dea8980-9d23-11eb-888c-8f4f7ece0cbf.png">
</p>
