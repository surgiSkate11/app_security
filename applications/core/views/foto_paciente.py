from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseForbidden
from applications.core.models import FotoPaciente, Paciente
from applications.core.forms.foto_paciente import FotoPacienteForm

class FotoPacienteListView(ListView):
    model = FotoPaciente
    template_name = 'core/pacientes/galeria_fotos.html'
    context_object_name = 'fotos'
    paginate_by = 12

    def get_queryset(self):
        paciente_id = self.kwargs.get('paciente_id')
        return FotoPaciente.objects.filter(paciente_id=paciente_id).order_by('-fecha_subida')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['paciente'] = get_object_or_404(Paciente, pk=self.kwargs.get('paciente_id'))
        context['form'] = FotoPacienteForm()
        return context

    def post(self, request, *args, **kwargs):
        paciente = get_object_or_404(Paciente, pk=kwargs.get('paciente_id'))
        form = FotoPacienteForm(request.POST, request.FILES)
        if form.is_valid():
            foto = form.save(commit=False)
            foto.paciente = paciente
            foto.save()
            return redirect('core:galeriafotos', paciente_id=paciente.id)
        # If not valid, re-render with errors
        fotos = FotoPaciente.objects.filter(paciente=paciente).order_by('-fecha_subida')
        return self.render_to_response({
            'paciente': paciente,
            'fotos': fotos,
            'form': form
        })

class FotoPacienteDeleteView(DeleteView):
    model = FotoPaciente
    template_name = 'core/pacientes/confirm_delete_foto.html'

    def get_success_url(self):
        return reverse_lazy('core:galeriafotos', kwargs={'paciente_id': self.object.paciente.id})

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.paciente.id != int(self.kwargs.get('paciente_id')):
            return HttpResponseForbidden()
        return super().delete(request, *args, **kwargs)
