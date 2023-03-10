import numpy as np

def sort_xy(x, y, ang_shift=0):
    
    'https://stackoverflow.com/questions/58377015/counterclockwise-sorting-of-x-y-data'

    x0 = np.mean(x)
    y0 = np.mean(y)

    r = np.sqrt((x-x0)**2 + (y-y0)**2)

    angles = np.where((y-y0) > 0, np.arccos((x-x0)/r), 2*np.pi-np.arccos((x-x0)/r))

    mask = np.argsort(angles)

    sort_deg = np.sort(np.degrees(angles))
    sort_deg_min_ind = np.argwhere(sort_deg > ang_shift)[0][0]

    rearr_mask = np.hstack((mask[sort_deg_min_ind:], mask[0:sort_deg_min_ind]))

    x_sorted = x[rearr_mask]
    y_sorted = y[rearr_mask]

    angles_sorted = np.where((y_sorted-y0) > 0, np.arccos((x_sorted-x0)/r), 2*np.pi-np.arccos((x_sorted-x0)/r))

    return x_sorted, y_sorted

def outline2map(outline, image, n_images, ang_shift, avg_range=0):

    avg_list = []
    total_val_list = []

    # Iterate through images
    for i in range(0, n_images):
        
        # Sort outline pixels clockwise
        x, y = (outline[i] == True).nonzero()
        x_sorted, y_sorted = sort_xy(x, y, ang_shift)

        val_list = []
        # Iterate through sorted pixels and extract pixel values
        for j in range(0, len(x_sorted)):
            val = image[i, x_sorted[j], y_sorted[j]]
            val_list.append(val)
            val_array = np.array(val_list)
        
        total_val_list.append(val_list)
        
        if avg_range > 0:
        
            # Average values within windows
            split_list = np.array_split(val_array, avg_range)
            split_mean = [np.mean(k) for k in split_list]

            avg_list.append(split_mean)
    
    if avg_range > 0:
        out = np.array(avg_list)
        
    else:
        out = total_val_list
        
    return out, x_sorted, y_sorted