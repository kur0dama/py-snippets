def j_nums(i,gt_man=False):
    """
    Takes an integer or float and returns a string of kanji representing the value.
    Required arguments:
        i: the number to be converted
    Optional arguments: 
        gt_man: an internal indicator; not to be supplied by user
    Returns:
        A string with kanji equating to the numeric value of input i
    """
    
    if type(i) not in (int, float):
        return None
    else:
        # identify decimals
        str_val = str(i)
        has_decimal = '.' in str_val
        outstring = ''
        # handle negative numbers
        if i<0: 
            outstring+='マイナス'
            i=abs(i)
        i=int(i//1)
        if i==0:
            outstring+='零'
        elif i>0:
            nums = {
                0:'', 1:'一', 2:'二', 3:'三', 4:'四', 5:'五',
                6:'六',  7:'七', 8:'八', 9:'九', 10:'十',
                100:'百', 1000:'千', 10000: '万', 
                100000000: '億', 1000000000000: '兆'
            }
            i=int(i//1)
            # handle portion of number >=10000
            for val in [1000000000000, 100000000, 10000]:
                n=i//val
                if n>0: 
                    outstring = outstring + j_nums(n, gt_man=True) + nums[val]
                    i=i%(n*val)
            # handle portion of number <10000
            for val in [1000,100,10]:
                n=i//val
                if n>0:
                    j = 0 if (n==1 and (gt_man==False or val<1000)) else n
                    outstring = outstring + nums[j] + nums[val]
                    i=i%(n*val)
            outstring = outstring + nums[i]
        # handle decimal
        if has_decimal:
            outstring+='・'
            dot_loc = str_val.index('.')+1
            decimal_chars = {
                0:'〇', 1:'一', 2:'二', 3:'三', 4:'四', 5:'五',
                6:'六',  7:'七', 8:'八', 9:'九'
            }
            outstring+=''.join([ decimal_chars[int(c)] for c in str_val[dot_loc:] ])
        return outstring
