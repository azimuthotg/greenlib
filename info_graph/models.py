from django.db import models

class Year(models.Model):
    year = models.IntegerField(unique=True)

    def __str__(self):
        return str(self.year)

class Month(models.Model):
    year = models.ForeignKey(Year, on_delete=models.CASCADE)
    month = models.IntegerField()
    month_name = models.CharField(max_length=255)

    class Meta:
        unique_together = ('year', 'month')

    def __str__(self):
        return f"{self.year.year}-{self.month:02d}"

class DataEntry(models.Model):
    month = models.ForeignKey(Month, on_delete=models.CASCADE)
    greenhouse_gas = models.FloatField()
    electricity = models.FloatField()
    diesel = models.FloatField()
    water = models.FloatField()
    landfill_waste = models.FloatField()
    paper_a4_a3 = models.FloatField()

    def __str__(self):
        return f"Data for {self.month}"
