from django.views.generic.list import ListView
from app.models import Todo
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from app.forms import TodoForm
from django.shortcuts import redirect, render, render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


@method_decorator(permission_required('app.list_app'))
def listar(request):
    porhacer = Todo.objects.all()
    return render(request, 'app/listar.html', {'porhacer':porhacer})

class TodoList(ListView):
    model = Todo

class TodoDetail(DetailView):
    model = Todo
    @method_decorator(permission_required('app.view_app'))
    def dispatch(self, *args, **kwargs):
        return super(TodoDetail, self).dispatch(*args, **kwargs)

class TodoCreate(CreateView):
    model = Todo
    form_class = TodoForm
    @method_decorator(permission_required('app.add_app'))
    def dispatch(self, *args, **kwargs):
        return super(TodoCreate, self).dispatch(*args, **kwargs)
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.save()
        return redirect(self.object)

class TodoUpdate(UpdateView):
    model = Todo
    form_class = TodoForm
    @method_decorator(permission_required('app.change_app'))
    def dispatch(self, *args, **kwargs):
        return super(TodoUpdate, self).dispatch(*args, **kwargs)

class TodoDelete(DeleteView):
    model = Todo
    @method_decorator(permission_required('app.delete_app'))
    def dispatch(self, *args, **kwargs):
        return super(TodoDelete, self).dispatch(*args, **kwargs)
    def get_success_url(self):
        # To do this because the success_url class variable isn't reversed...
        return reverse('app_list')
def ingresar(request):
    if not request.user.is_anonymous():
        return HttpResponseRedirect('/index')
    if request.method == 'POST':
        formulario = AuthenticationForm(request.POST)
        if formulario.is_valid:
            usuario = request.POST['username']
            clave = request.POST['password']
            acceso = authenticate(username=usuario, password=clave)
            if acceso is not None:
                if acceso.is_active:
                    login(request, acceso)
                    return HttpResponseRedirect('/')
                else:
                    return render_to_response('nome.html',
                                              context_instance=RequestContext(request))
            else:
                return render_to_response('nome.html',
                                          context_instance=RequestContext(request))
    else:
        formulario = AuthenticationForm()
    return render_to_response('login.html', {'formulario': formulario},
                              context_instance=RequestContext(request))
@login_required(login_url='/ingresar')
def privado(request):
    usuario = request.user
    return render_to_response('anonymus.html', {'usuario': usuario},
                              context_instance=RequestContext(request))

@login_required(login_url='/ingresar')
def cerrar(request):
    logout(request)
    return HttpResponseRedirect('/')


