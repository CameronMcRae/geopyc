from django.shortcuts import render, get_object_or_404
from django.template import RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from control.models import Method, Run 
import socket, pickle, random
import datetime

def run_history(request):
    latest_run_list = Run.objects.order_by('-run_date')
    template = loader.get_template('control/run_index.html')
    context = RequestContext(request, {'latest_run_list': latest_run_list})
    return HttpResponse(template.render(context))

def index(request):
    latest_method_list = Method.objects.order_by('-pub_date')
    template = loader.get_template('control/index.html')
    context = RequestContext(request, {
        'latest_method_list': latest_method_list, 
    })
    return HttpResponse(template.render(context))

def detail(request, method_id):
    method = get_object_or_404(Method, pk=method_id)
    template = loader.get_template('control/detail.html')
    context = RequestContext(request, {'method': method})
    return HttpResponse(template.render(context))

def results(request):
    method_id = 1
    method = get_object_or_404(Method, pk=method_id)
    force = random.random()*40
    cycle = random.randint(1, 10)
    volume = random.random()*10
    density = float(method.mass) / volume
    date_time = datetime.datetime.today()
    run = Run()
    run.method = method
    run.force = force
    run.cycle = cycle
    run.volume = volume
    run.density = density
    run.run_date = date_time
    run.save()
    msg = {'method_id': method_id, 'method': method, 'force': force, 'cycle': cycle, 
           'volume': volume, 'density': density}
    context = RequestContext(request, msg)
    template = loader.get_template('control/results.html')
    return HttpResponse(template.render(context))

def run(request, method_id):
    method = get_object_or_404(Method, pk=method_id)

    try:
        s = socket.socket()         
        host = socket.gethostname()
        port = 12345                
        s.connect((host, port))
        msg = pickle.dumps((method_id, method))
        s.sendall(msg)
        s.close()
    except:
        raise Exception("Server not running.")
    return HttpResponseRedirect(reverse('control:analysis'))
    
    

def analysis(request):
    #Get information from server
#     try:
#         s = socket.socket()
#         host = socket.gethostname()
#         port = 12345
#         s.connect((host, port))
#         s.sendall('1'.encode())
#         reply = s.recv(1024)
#         reply = pickle.loads(reply)
#         s.close()
#     except: 
#         raise Exception("Server not running.")
    method_id = 1
    method = get_object_or_404(Method, pk=method_id)
    force = random.random()*40
    cycle = random.randint(1, 10)
    volume = random.random()*10
    msg = {'method_id': method_id, 'method': method, 'force': force, 'cycle': cycle, 'volume': volume }
    template = loader.get_template('control/analysis.html')
    context = RequestContext(request, msg)
    #return HttpResponse(template.render(context))
    return HttpResponseRedirect(reverse('control:results'))
    
    

