from django.db import models
import django.utils
import datetime

class Method(models.Model):
    RUN_TYPE_CHOICES = (('ZD', 'Zero-Depth'), ('BD', 'Blank-Data'), ('CB', 'Calibration'), ('SM', 'Sample'))
    DIAMETER_CHOICES = (('12.7', '12.7'), ('19.1', '19.1'), ('25.4', '25.4'), ('38.1', '38.1'), ('50.8', '50.8'))
    
    Run_Type = models.CharField(max_length=200, choices=RUN_TYPE_CHOICES, default='')
    Operator_Name = models.CharField(max_length=200, default='')
    Sample_Name = models.CharField(max_length=200, default='')
    Diameter = models.CharField(max_length=200, choices=DIAMETER_CHOICES, default='')
    mass = models.DecimalField(max_digits=5, decimal_places=1, default=0.0)
    pub_date = models.DateTimeField('date published', default=django.utils.timezone.now())

    def __str__(self):
        name = (" Run Type: " + self.get_Run_Type_display(), " Operator Name: " +self.Operator_Name, 
                " Sample Name: " + self.Sample_Name, " Diameter: " + self.get_Diameter_display(), 
                " Mass: " + str(self.mass), " Date Published: " +str(self.pub_date))
        return str(name)

class Run(models.Model):
    method = models.ForeignKey(Method, default=Method())
    cycle = models.IntegerField(default=0)
    force = models.DecimalField(max_digits=5, decimal_places=1, default=0.0)
    volume = models.DecimalField(max_digits=5, decimal_places=1, default=0.0)
    density = models.DecimalField(max_digits=5, decimal_places=1, default=0.0)
    run_date = models.DateTimeField('date run', default=django.utils.timezone.now()) 
        
    def __str__(self):
        name = (" Method: " + str(self.method), " Cycle: " + self.cycle, " Force: " + self.get_force_display(),
         " Volume: " + self.get_volume_display(), " Density: " + self.get_density_display(), 
         " Date Run: " + str(self.get_run_date_display()))
        return str(name)



        
        
    