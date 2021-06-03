import logging
import matplotlib.pyplot as plt
import pmdarima as pm
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX
import math
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score 
from sklearn.metrics import mean_absolute_error 
from sklearn.model_selection import train_test_split

class arimaMaker:    
    def __init__(self,num_prediction_days,p,d,q,data):
        self.logger = logging.getLogger('arimaMaker')
        # Select how many days of the week predictions will be made on
        self.num_days = num_prediction_days # Predictions will be made on 3 days 
    
        if self.num_days <= 3:
        # Convert selection to a positional index in order to make the test train split 
            index_limit = len(data) - len(df['Hour'].unique())*self.num_days 

        # Implement the test train split by plugging in the specified index limit 
        # This sets the cieling index for train and the floor index for test
            train, self.test = X[:index_limit], X[index_limit:] 
            
        else:
            index_limit = len(data) - len(df['Hour'].unique())*(7-self.num_days)
            train, self.test = X[index_limit:], X[:index_limit]
            

        self.history = [x for x in train]                  # Declares the history as the "training set"
        self.predictions = list()                          # Declares a list for the predictions to be stored in
    
        self.p = p
        self.d = d
        self.q = q
        self.DOW = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']
        self.residuals = None 
        self.logger.info('creating an instance of arimaMaker') 
        
    def train(self):
        self.logger.info('training model')
        for t in range(len(self.test)): 

            model = ARIMA(self.history, order=(self.p,self.d,self.q))      # ARIMA function
            model_fit1 = model.fit(disp=0)                   
            self.residuals = model_fit1.resid
            output = model_fit1.forecast()
            yhat = output[0]
            self.predictions.append(yhat)                   # Appended array of the output or "predictions"
            obs = self.test[t]
            self.history.append(obs)                        # Appended array of the history or "training set"                    
            #print('predicted=%f, expected=%f' % (yhat, obs))
        self.logger.info('model created')
        
    def plotter(self):
        fig, ax = plt.subplots(2,2, figsize=(15,9), gridspec_kw = {'wspace':0.2, 'hspace':0.4})

        ax[0,0].plot(self.residuals)
        ax[0,0].set_title('Stationarized Data')

        density = gaussian_kde(self.residuals)
        xs = np.linspace(0,24,240)
        ax[0,1].plot(xs,density(xs))
        ax[0,1].set_title('Residual Errors KDE')

        sm.graphics.tsa.plot_acf(self.residuals, lags=160, ax=ax[1,0])
        sm.graphics.tsa.plot_pacf(self.residuals, lags=30, ax=ax[1,1])

        plt.show() 

        # Create a plot comparing the test and training data results 
        fig, ax1 = plt.subplots(1,1, figsize=(15,5))
        ax1.plot(self.test[:-1], color='blue', lw=2, label='Test Data')
        ax1.plot(self.predictions[1:], color='red', lw=2, label='Predictions')

        # Label and format plot 
        ax1.set_ylabel('Hourly Call Volume',fontsize=22)
        ax1.set_title('ARIMA Model Comparison',fontsize=24)

        ax1.margins(x=0) # Removes gaps between x-ticks
        ax1.grid(True, color='k', alpha=1)
        ax1.legend(prop={'size': 12},shadow=True) 

        # Make recurrent list for the time labels
        xticks_Phone = np.arange(0,len(self.test),6) # Time label Positional markers
        extended_time_labels = duplicate([' 00:00',' 06:00',' 12:00',' 18:00'],self.num_days) # Recurrent list of times to label each day

        # Format the x and y-tick labels 
        plt.xticks(xticks_Phone, extended_time_labels, rotation=45, fontsize=17, ha='right', rotation_mode='anchor') #x-axis tick marks
        plt.yticks(fontsize=20)

        # Create a second x-axis for adding the DOW labels  
        ax2 = ax1.twiny()

        # Label and format second axis
        xticks_DOW = np.arange(12,len(self.test),24) # DOW label positional markers
        ax2.set_xticks(xticks_DOW)
        
        if self.num_days <= 3:    
            ax2.set_xticklabels(self.DOW[len(self.DOW)-self.num_days:])
        else:
            ax2.set_xticklabels(self.DOW[:self.num_days])
        ax2.tick_params(axis='x', labelsize=20, color='w')

        # Set the position of the second axis                 
        ax2.xaxis.set_ticks_position('bottom') 
        ax2.xaxis.set_label_position('bottom') 
        ax2.spines['bottom'].set_position(('outward',70)) 
        ax2.spines['bottom'].set_color('w') # Hide second x-axis
        plt.setp(ax2.get_xticklabels(), color='k') # Set DOW label color 
        ax2.set_xlim(ax1.get_xlim())    
        
    def stats(self):
        # Calculate the stats 
        error = mean_squared_error(self.test[:len(self.test)-1], self.predictions[1:])
        square_error = math.sqrt(error)
        MAPE = mean_absolute_error(self.test[:len(self.test)-1], self.predictions[1:])
        r2 = r2_score(self.test[:len(self.test)-1], self.predictions[1:])
        
        # Report the stats 
        print('Trained On: '+str("{:0.1f}".format((len(self.DOW)-self.num_days)*100/len(self.DOW)))+' %'+
              'Tested On: '+str("{:0.1f}".format(self.num_days*100/len(self.DOW)))+' %')
        print('\n')
        print('Test MSE: %.3f' % error)
        print('Test RSME: %.3f' % square_error)
        print('Test MAPE: %.3f' % MAPE)
        print('Test R\u00B2: %.3f' % r2)
        self.logger.info('model stats calculated')
        
    def train_and_display(self):
        self.train()
        self.plotter()
        self.stats()