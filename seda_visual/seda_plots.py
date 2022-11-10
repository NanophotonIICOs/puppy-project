import plotly.graph_objects as go
import numpy as np
from plotly.subplots import make_subplots
from seda_utils import utils



def zmap(exptype):
    z = exptype.T
    nx, ny = z.shape[1], z.shape[0]
    x, y = np.meshgrid(np.arange(0, nx, 1), np.arange(0, ny, 1))
    xx = np.arange(0, nx, 1)
    yy = np.arange(0, ny, 1)
    offs = np.min(z)*0.13
    if np.min(z)-offs > 1.e-4:
        z_offset=(np.min(z)-offs)*np.ones(z.shape)#
    else:
        z_offset=(np.min(z)+offs)*np.ones(z.shape)#

    x_offset=-np.min(xx)*np.ones(z.shape)
    y_offset=np.min(yy)*np.ones(z.shape)
    proj_z=lambda x, y, z: z#projection in the z-direction
    colorsurfz=proj_z(x,y,z)
    proj_x=lambda x, y, z: x
    colorsurfx=proj_z(x,y,z)
    proj_y=lambda x, y, z: y
    colorsurfy=proj_z(x,y,z)

    class Results(): pass
    results = Results()
    results.colorsurfz=  colorsurfz
    results.z_offset = z_offset
    results.x = x
    results.y = y
    return results




def fig_3d_2d_layout(data,template,attrs,pixel,color,**kwargs):
    
    if  'tick_step' in kwargs:
        tick_step = kwargs.pop('tick_step')
    else:
        tick_step = 1
        
    z = data
    nx = z.shape[0]
    ny = z.shape[1]
    xm,ym = np.meshgrid(np.arange(0, nx, 1), np.arange(0, ny, 1))
    x = np.arange(0, nx, 1)
    y = np.arange(0, ny, 1)
    expsoffsets = zmap(z)
    
    if attrs:
        xi =  int(attrs['Inicio X'])
        xf =  int(round(attrs['fin X ']/attrs['paso']))
        print(xf)
        yi =  int(attrs['Inicio Y'])
        yf =  int(round(attrs['fin Y ']/attrs['paso']))    
        step = attrs['paso']
        xt = np.arange(xi,xf,tick_step)
        yt = np.arange(yi,yf,tick_step)
        xtl = xt*step
        ytl = yt*step
    else:
        xi =  x[0]
        xf =  x[-1]
        yi =  y[0]
        yf =  y[-1]
        step = 1
        xt = np.arange(xi,xf,tick_step)
        yt = np.arange(yi,yf,tick_step)
        xtl = xt*step
        ytl = yt*step
        # utils.error_alert()
        
        
    
    fig = make_subplots(
            rows=2, cols=2, 
            column_widths=[0.6, 0.4],
            row_heights=[0.6, 0.4],
            specs=[[{'type': 'surface','rowspan':2},{'type': 'contour'}],
                [None, {'type':'scatter'}]],
            horizontal_spacing=0.03,
            vertical_spacing=0.05,
            shared_xaxes=True,
            
            )


        # Generate data
    fig.add_trace(go.Surface(z=data.T,showscale=False,colorscale=color),row=1, col=1)
    fig.add_trace(go.Heatmap(z=data.T,connectgaps=True, zsmooth='best',colorscale=color),row=1, col=2)
    fig.add_trace(go.Surface(z=list(expsoffsets.z_offset),  # type: ignore
                x=list(expsoffsets.x),
                y=list(expsoffsets.y),
                colorscale=color,
                showscale=False, 
                 surfacecolor=expsoffsets.colorsurfz),row=1, col=1)
    
    pixel_line_profile = go.Scatter(x=x,y=z[:,pixel],mode='lines+markers',marker_line_width=2,marker_size=10,)
    pixel_line = go.Scatter(x=[xi,xf],y=[pixel,pixel],marker_line_width=2,marker_size=10)
    fig.add_trace(pixel_line_profile,row=2,col=2)
    fig.add_trace(pixel_line,row=1,col=2)

    fig.update_layout(
        showlegend=False,
            template=template,
            width=900,
            height=550,
            margin=dict(l=5, r=5, b=25, t=20),
            font=dict(
            family="Latin Modern Roman,serif",
            color='white',
            size=13,
        ),   
            plot_bgcolor='rgba(0,0,0,0)',
        xaxis2 = dict(title='x (nm)',tickvals=xt,ticktext=xtl,range=[xi,xf]),
        yaxis1 = dict(title=' ',tickvals=[],range=[yi,yf]),
         scene=dict(
            xaxis=dict(title = 'x (nm)',tickmode='array',ticktext=xtl,tickvals=xt,tickprefix= "nm",),
            yaxis=dict(title = 'y (nm)',tickmode='array',ticktext=ytl,tickvals=yt,tickprefix= "nm",),
            zaxis=dict()

    ),
    )
    return fig
