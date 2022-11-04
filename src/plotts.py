import numpy as np 
import h5py as h5
import glob
from os import walk
import time
import plotly.graph_objects as go
from plotly.subplots import make_subplots



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




class plotts:
    def __init__(self,afm,lockin,multimeter,step=1):
        self.afm = afm
        self.lockin = lockin
        self.multimeter = multimeter
        self.step = step
        self.nx = self.afm.shape[0]
        self.ny = self.afm.shape[1]
        self.xm, self.ym = np.meshgrid(np.arange(0, self.nx, 1), np.arange(0, self.ny, 1))
        self.x = np.arange(0, self.nx, 1)
        self.y = np.arange(0, self.ny, 1)
        self.xt =np.arange(self.x[0],self.x[-1],2)
        self.yt =np.arange(self.y[0],self.y[-1],2)
        self.xtl = self.xt*self.step
        self.ytl = self.yt*self.step

    def plotting(self,**kwargs):
        fig = make_subplots(
                rows=1, cols=3,
                specs=[[{'type': 'surface'}, {'type': 'surface'},{'type': 'surface'}]],
                print_grid=False, 
                shared_xaxes=True,
                shared_yaxes=True,
                horizontal_spacing=0.0,)

        axis = dict(
                    showbackground=True,
                    #backgroundcolor="rgb(230, 230,230)",
                    showgrid=False,
                    zeroline=False,
                    showline=False
                    )

        self.exp2plots = [self.afm,self.lockin,self.multimeter]
        for i,experiment in enumerate(self.exp2plots):
            fig.add_trace(
                go.Surface(z=experiment.T, colorscale='Plotly3',showscale=False, reversescale=True,),row=1, col=i+1)
            #fig.update_traces(contours_x=dict(show=True, usecolormap=True, project_x=True))
            #fig.update_traces(contours_y=dict(show=True, usecolormap=True, project_y=True))
            fig.add_trace(go.Surface(z=list(zmap(experiment).z_offset),  # type: ignore
                x=list(zmap(experiment).x),
                y=list(zmap(experiment).y),
                colorscale='Plotly3',showscale=False, reversescale=True,
                 surfacecolor=zmap(experiment).colorsurfz,  # type: ignore
               ),row=1, col=i+1)


        fig.update_layout(
            #template="plotly_dark",
            width=1300,
            autosize=True,
            margin=dict(l=5, r=5, b=25, t=20),
            font=dict(
                family="Computer Modern Roman,serif",
                color='white',
                size=13,
            ),
            scene=dict(
            xaxis=dict(axis,title = 'x (nm)',tickmode='array',ticktext=self.xtl,tickvals=self.xt,tickprefix= "nm",),
            yaxis=dict(axis,title = 'y (nm)',tickmode='array',ticktext=self.ytl,tickvals=self.yt,tickprefix= "nm",),
            zaxis=dict(axis,))
        )
        return fig

    def plotall(self,exp='afm',**kwargs):
        fig = make_subplots(
                rows=2, cols=2, 
                column_widths=[0.6, 0.4],
                row_heights=[0.5, 0.5],
                specs=[[{'type': 'surface','rowspan':2},{'type': 'contour'}],
                    [None, {'type':'scatter'}]],
                horizontal_spacing=0.075,
                vertical_spacing=0.01,
                shared_xaxes=True,
                print_grid=False,
                )

        axis = dict(
                    showbackground=True,
                    #backgroundcolor="rgb(230, 230,230)",
                    showgrid=False,
                    zeroline=False,
                    showline=False
                    )
            # Generate data
        if exp=='afm':
            expsoffsets = zmap(self.afm)
            fig.add_trace(go.Surface(z=self.afm.T, colorscale='Plotly3',showscale=False, reversescale=True),row=1, col=1)
            fig.add_trace(go.Heatmap(z=self.afm.T, colorscale='Plotly3',reversescale=True,connectgaps=True, zsmooth='best'),row=1, col=2)
            fig.add_trace(go.Scatter(x=self.xm[0],y=self.afm[:,5],
                                    mode='lines',
                                    name='%s Profile'%(exp.upper()),
                                    line=dict(color='royalblue',width=3)),row=2,col=2)
            fig.add_trace(go.Surface(z=list(expsoffsets.z_offset),  # type: ignore
                x=list(expsoffsets.x),
                y=list(expsoffsets.y),
                colorscale='Plotly3',
                showscale=False, reversescale=True,
                 surfacecolor=expsoffsets.colorsurfz),row=1, col=1)

        elif exp=='lockin':
            expsoffsets = zmap(self.lockin)
            fig.add_trace(go.Surface(z=self.lockin.T, colorscale='Plotly3',showscale=False, reversescale=True),row=1, col=1)
            fig.add_trace(go.Heatmap(z=self.lockin.T, colorscale='Plotly3',reversescale=True,connectgaps=True, zsmooth='best'),row=1, col=2)
            fig.add_trace(go.Scatter(x=self.xm[0],y=self.lockin[:,5],
                                    mode='lines',
                                    name='%s Profile'%(exp.upper()),
                                    line=dict(color='royalblue',width=3)),row=2,col=2)
            fig.add_trace(go.Surface(z=list(expsoffsets.z_offset),  # type: ignore
                x=list(expsoffsets.y),
                y=list(expsoffsets.x),
                colorscale='Plotly3',
                showscale=False, reversescale=True,
                surfacecolor=expsoffsets.colorsurfz),row=1, col=1)

        elif exp=='multimeter':
            expsoffsets = zmap(self.multimeter)
            fig.add_trace(go.Surface(z=self.multimeter.T, colorscale='Plotly3',showscale=False, reversescale=True),row=1, col=1)
            fig.add_trace(go.Heatmap(z=self.multimeter.T, colorscale='Plotly3',reversescale=True,connectgaps=True, zsmooth='best'),row=1, col=2)
            fig.add_trace(go.Scatter(x=self.xm[0],y=self.multimeter[:,5],
                                    mode='lines',
                                    name='%s Profile'%(exp.upper()),
                                    line=dict(color='royalblue',width=3)),row=2,col=2)
            fig.add_trace(go.Surface(z=list(expsoffsets.z_offset),  # type: ignore
                x=list(expsoffsets.y),
                y=list(expsoffsets.x),
                colorscale='Plotly3',
                showscale=False, reversescale=True,
                 surfacecolor=expsoffsets.colorsurfz),row=1, col=1)

        fig.update_layout(
            autosize=True,
            margin=dict(l=5, r=5, b=25, t=20),
            width=900,height=500,
            font=dict(
                family="Times New Roman",
                color='white',
                size=13,
            ),   
            xaxis2 = dict(title='x (nm)',tickvals=self.xt,ticktext=self.xtl),
            yaxis1 = dict(title=' ',tickvals=[]),
            scene=dict(
            xaxis=dict(axis,title = 'x (nm)',tickmode='array',ticktext=self.xtl,tickvals=self.xt,tickprefix= "nm",),
            yaxis=dict(axis,title = 'y (nm)',tickmode='array',ticktext=self.ytl,tickvals=self.yt,tickprefix= "nm",),
            zaxis=dict(axis,)
                    )
        )
        # fig.update_layout({
        #     'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        #     'paper_bgcolor': 'rgba(0, 0, 0, 0)',
        #     })
        return fig


