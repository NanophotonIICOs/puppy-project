import numpy as np 
import h5py as h5
import glob
from os import walk
import time
import plotly.graph_objects as go
from plotly.subplots import make_subplots

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
                specs=[[{'type': 'surface'}, {'type': 'surface'},{'type': 'surface'}]],print_grid=False, shared_xaxes=True,shared_yaxes=True,)

        self.exp2plots = [self.afm,self.lockin,self.multimeter]
        for i,expriment in enumerate(self.exp2plots):
            fig.add_trace(
                go.Surface( z=expriment, colorscale='Plotly3',showscale=False, reversescale=True,),row=1, col=i+1)
            fig.update_traces(contours_x=dict(show=True, usecolormap=True, project_x=True))
            fig.update_traces(contours_y=dict(show=True, usecolormap=True, project_y=True))


        fig.update_layout(
            #template="plotly_dark",
            #width=1200,
            font=dict(
                family="Computer Modern Roman,serif",
                color='white',
                size=13,
            ),
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
            # Generate data
        if exp=='afm':
            fig.add_trace(go.Surface(z=self.afm.T, colorscale='Plotly3',showscale=False, reversescale=True),row=1, col=1)
            fig.add_trace(go.Heatmap(z=self.afm.T, colorscale='Plotly3',reversescale=True,connectgaps=True, zsmooth='best'),row=1, col=2)
            fig.add_trace(go.Scatter(x=self.xm[0],y=self.afm[:,5],
                                    mode='lines',
                                    name='%s Profile'%(exp.upper()),
                                    line=dict(color='royalblue',width=3)),row=2,col=2)
        elif exp=='lockin':
            fig.add_trace(go.Surface(z=self.lockin.T, colorscale='Plotly3',showscale=False, reversescale=True),row=1, col=1)
            fig.add_trace(go.Heatmap(z=self.lockin.T, colorscale='Plotly3',reversescale=True,connectgaps=True, zsmooth='best'),row=1, col=2)
            fig.add_trace(go.Scatter(x=self.xm[0],y=self.lockin[:,5],
                                    mode='lines',
                                    name='%s Profile'%(exp.upper()),
                                    line=dict(color='royalblue',width=3)),row=2,col=2)
        elif exp=='multimeter':
            fig.add_trace(go.Surface(z=self.multimeter.T, colorscale='Plotly3',showscale=False, reversescale=True),row=1, col=1)
            fig.add_trace(go.Heatmap(z=self.multimeter.T, colorscale='Plotly3',reversescale=True,connectgaps=True, zsmooth='best'),row=1, col=2)
            fig.add_trace(go.Scatter(x=self.xm[0],y=self.multimeter[:,5],
                                    mode='lines',
                                    name='%s Profile'%(exp.upper()),
                                    line=dict(color='royalblue',width=3)),row=2,col=2)

        fig.update_layout(
            autosize=True,
            margin=dict(l=5, r=5, b=25, t=20),
            width=800,height=500,
            font=dict(
                family="Times New Roman",
                color='white',
                size=13,
            ),   
            xaxis2 = dict(title='x (nm)',tickvals=self.xt,ticktext=self.xtl),
            yaxis1 = dict(title=' ',tickvals=[]),

            scene=dict(
            xaxis=dict(title = 'x (nm)',tickmode='array',ticktext=self.xtl,tickvals=self.xt,tickprefix= "nm",),
            yaxis=dict(title = 'y (nm)',tickmode='array',ticktext=self.ytl,tickvals=self.yt,tickprefix= "nm",)),
        )
        # fig.update_layout({
        #     'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        #     'paper_bgcolor': 'rgba(0, 0, 0, 0)',
        #     })
        return fig
