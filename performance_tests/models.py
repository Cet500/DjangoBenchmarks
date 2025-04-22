from django.db import models as m


class TestResult( m.Model ):
    test_id        = m.CharField( max_length = 100, verbose_name = 'ID теста' )
    test_name      = m.CharField( max_length = 100, verbose_name = 'Название' )
    parameters     = m.CharField( max_length = 200, verbose_name = 'Параметры' )
    execution_time = m.FloatField( verbose_name = 'Время выполнения' )

    python_version = m.CharField( max_length = 50, verbose_name = 'Версия Python' )
    django_version = m.CharField( max_length = 50, verbose_name = 'Версия Django' )

    os             = m.CharField( max_length = 100, verbose_name = 'OS' )
    cpu            = m.CharField( max_length = 150, verbose_name = 'CPU' )
    memory         = m.IntegerField( verbose_name = 'RAM' )
    gpu            = m.CharField( max_length = 150, verbose_name = 'GPU' )

    created_at     = m.DateTimeField( auto_now_add = True )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.test_id} ({self.parameters}) - {self.execution_time:.2f}s"
