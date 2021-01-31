
        ''' pk=self.kwargs.get("pk")
        di = self.kwargs.get("di")
        
        dis=get_object_or_404(Disease,pk=di)
        
        pestiside=Pestiside.objects.get(pk=pk,disease=dis)
    

        
        if request.method=='POST':
            user = request.user
            form= ReviewForm(request.POST)
            if form.is_valid():
                form.author = request.user
                form.pes_id = pk
                form.save()
                
                
                #comment=form.cleaned_data.get('comment')
                #new_review=Review.objects.create(author=user,pes_id=pestiside_id,comment=comment)
                #new_review.save()  
            return redirect('diagnose:pestiside')  '''