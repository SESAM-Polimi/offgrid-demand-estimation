
### EXP 1
EPOCHS = 500
BATCH_SIZE = 64
Features = all (61)
sampler: Random Under Sampler
Threshold=0.5
EARLY_STOPPING = Without


Validation
              precision    recall  f1-score   

         0.0       0.89      0.98      0.93  
         1.0       0.92      0.61      0.73  

    accuracy                           0.89  

```python
model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(FEATURE_NUM,)),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')
])
```



### EXP 2
EPOCHS = 1000
BATCH_SIZE = 512
OPTIMIZER = tf.keras.optimizers.Adam(learning_rate=0.001)
Features = all (61)
sampler: Random Over Sampler
Threshold=0.5
EARLY_STOPPING = NO

Validation
              precision    recall  f1-score   

         0.0       0.98      0.70      0.81   
         1.0       0.51      0.96      0.66   

    accuracy                           0.76   
   

```python
model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(FEATURE_NUM,)),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')
])
```


## EXP 3

Training
              precision    recall  f1-score   

         0.0       0.94      0.86      0.90   
         1.0       0.87      0.95      0.91   

    accuracy                           0.91   
****************************************************************************************************
Validation
              precision    recall  f1-score  

         0.0       0.98      0.84      0.90  
         1.0       0.66      0.94      0.77  

    accuracy                           0.87  


### Params
```python
BATCH_SIZE = 1024
EPOCHS = 1000
OPTIMIZER = tf.keras.optimizers.Adam(learning_rate=0.001)
LOSS = tf.keras.losses.BinaryCrossentropy()
PATIENCE = 100
EARLY_STOPPING = tf.keras.callbacks.EarlyStopping(
    monitor='val_f2_score',    
    patience=PATIENCE,         
    restore_best_weights=True, 
    mode='max'
)

CALLBACKS = [
    EARLY_STOPPING,
]
Features = all
THRESHOLD = 0.5

```
### Model 
```python
model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(FEATURE_NUM,)),
    tf.keras.layers.Dense(128),
    tf.keras.layers.BatchNormalization(),  
    tf.keras.layers.ReLU(),
    tf.keras.layers.Dense(128),
    tf.keras.layers.BatchNormalization(),  
    tf.keras.layers.ReLU(),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')
])
```






## EXP 4
### PARAMS
```python

BATCH_SIZE = 1024
EPOCHS = 1000 # Stopped at 882
OPTIMIZER = tf.keras.optimizers.Adam(learning_rate=0.001)
LOSS = tf.keras.losses.BinaryCrossentropy()
PATIENCE = 250
EARLY_STOPPING = tf.keras.callbacks.EarlyStopping(
    monitor='val_precision',    # Metric to monitor (e.g., validation loss)
    patience=PATIENCE,            # Number of epochs to wait for improvement
    restore_best_weights=True,  # Restore weights from the best epoch
    mode='max',
    start_from_epoch=250
)

reduce_lr = tf.keras.callbacks.ReduceLROnPlateau(
    monitor='val_f2_score',  # Metric to monitor
    factor=0.9,          # Reduce learning rate by this factor (50%)
    patience=PATIENCE,          # Wait for 3 epochs of no improvement
    min_lr=1e-6,          # Minimum learning rate
    mode='max'
)

CALLBACKS = [
    EARLY_STOPPING, 
    # reduce_lr
]

```
Features = all
THRESHOLD = 0.4

### Model 

```python
initializer = tf.keras.initializers.GlorotNormal(21)  
regularizer = None

model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(FEATURE_NUM,)),
    tf.keras.layers.Dense(128, kernel_initializer=initializer, kernel_regularizer=regularizer),
    tf.keras.layers.BatchNormalization(),  
    tf.keras.layers.ReLU(),
    tf.keras.layers.Dense(128,kernel_initializer=initializer, kernel_regularizer=regularizer),
    tf.keras.layers.BatchNormalization(),  
    tf.keras.layers.ReLU(),
    tf.keras.layers.Dense(128,kernel_initializer=initializer,
                           kernel_regularizer=regularizer,
                           activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')
])
```

### Results
Training
              precision    recall  f1-score   

         0.0       0.82      0.93      0.87   
         1.0       0.92      0.80      0.86   

    accuracy                           0.87   
   

****************************************************************************************************
Validation
              precision    recall  f1-score   

         0.0       0.93      0.91      0.92   
         1.0       0.75      0.79      0.77   

    accuracy                           0.88   
   

