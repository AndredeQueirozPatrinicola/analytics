# AlunosGraduacao.objects.using('etl').filter(alunos_graduacao__situacao='ativo').values('estadoNascimento').annotate(count=Count('*')).order_by('estadoNascimento')