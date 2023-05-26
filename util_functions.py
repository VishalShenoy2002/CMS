def allowed_file(filename:str,extensions:set):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in extensions
