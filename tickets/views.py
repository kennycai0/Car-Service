from django.views import View
from django.http.response import HttpResponse
from django.shortcuts import render, redirect

line_of_cars = {
    "change_oil": [],
    "inflate_tires": [],
    "diagnostic": []
}
ticket_number = 0
next_ticket = 0


def calculate_time(ticket_type):
    minutes_to_wait = 0
    minutes_to_change_oil = 2 * len(line_of_cars['change_oil'])
    minutes_to_inflate_tires = 5 * len(line_of_cars['inflate_tires'])
    minutes_to_diagnostic = 30 * len(line_of_cars['diagnostic'])
    if ticket_type == 'change_oil':
        minutes_to_wait = minutes_to_change_oil
    elif ticket_type == 'inflate_tires':
        minutes_to_wait = minutes_to_inflate_tires + minutes_to_change_oil
    elif ticket_type == 'diagnostic':
        minutes_to_wait = minutes_to_diagnostic + minutes_to_inflate_tires + minutes_to_change_oil
    return minutes_to_wait


class WelcomeView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('<h2>Welcome to the Hypercar Service!</h2>')


class MenuView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'tickets/menu.html')


class TicketView(View):

    def get(self, request, *args, **kwargs):
        global ticket_number
        ticket_type = kwargs['ticket_type']
        minutes_to_wait = calculate_time(ticket_type)
        ticket_number += 1
        line_of_cars[ticket_type].append(ticket_number)
        context = {
            "ticket_number": ticket_number,
            "minutes_to_wait": minutes_to_wait
        }
        return render(request, 'tickets/ticket.html', context)


class ProcessingView(View):
    def get(self, request, *args, **kwargs):
        oil_len = len(line_of_cars['change_oil'])
        tires_len = len(line_of_cars['inflate_tires'])
        diagnostic_len = len(line_of_cars['diagnostic'])
        context = {
            "oil_len": oil_len,
            "tires_len": tires_len,
            "diagnostic_len": diagnostic_len
        }
        return render(request, 'tickets/processing.html', context)

    def post(self, request, *args, **kwargs):
        global next_ticket
        if len(line_of_cars['change_oil']) > 0:
            next_ticket = line_of_cars['change_oil'].pop(0)
        elif len(line_of_cars['inflate_tires']) > 0:
            next_ticket = line_of_cars['inflate_tires'].pop(0)
        elif len(line_of_cars['diagnostic']) > 0:
            next_ticket = line_of_cars['diagnostic'].pop(0)
        return redirect('/next')


class NextView(View):
    def get(self, request, *args, **kwargs):
        context = {"ticket_number": next_ticket}
        return render(request, 'tickets/next.html', context)
