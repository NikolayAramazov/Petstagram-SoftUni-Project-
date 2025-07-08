from django.shortcuts import render, redirect, get_object_or_404
from pets.forms import PetForm
from pets.models import Pets
from photos.models import Photo

def add_pet(request):
    if request.method == "POST":
        add_pet_form = PetForm(request.POST, request.FILES)
        if add_pet_form.is_valid():
            pet = add_pet_form.save(commit=False)
            pet.owner = request.user
            pet.save()
            return redirect('accounts:home')
    else:
        add_pet_form = PetForm()

    return render(request, 'pets/pet-add-page.html', {'form': add_pet_form})

def pet_details(request, pk):
    pet = get_object_or_404(Pets, pk=pk)
    photos = Photo.objects.filter(tagged_pet=pet).select_related('owner').prefetch_related('tagged_pet')

    return render(request, 'pets/pet-details-page.html', {'pet': pet, 'photos': photos})

def pet_edit(request, pk):
    pet = get_object_or_404(Pets, pk=pk)

    if request.method == "POST":
        edit_pet_form = PetForm(request.POST, request.FILES, instance=pet)
        if edit_pet_form.is_valid():
            edit_pet_form.save()
            return redirect('pets:pet_details', pk=pet.pk)
    else:
        edit_pet_form = PetForm(instance=pet)

    return render(request, 'pets/pet-edit-page.html', {'form': edit_pet_form})

def pet_delete(request, pk):
    pet = get_object_or_404(Pets, pk=pk)

    if request.method == "POST":
        pet.delete()
        return redirect('accounts:profile_details', pk=pet.owner.pk)

    return render(request, 'pets/pet-delete-page.html', {'pet': pet})

