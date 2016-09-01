void wavegraphs(char* fname, int event)
{
    TFile* tf = new TFile(fname);
    TTree* tree = (TTree*)tf->Get("Data");
    TCanvas *c1 = new TCanvas("c1", "I hate root", 200, 10, 700, 500);
    int wf0[512], wf1[512], wf2[512], wf3[512], tt[512];
    for(int i=0; i<512; i++){tt[i] = i;}
    tree->SetBranchAddress("waveform0", wf0);
    tree->SetBranchAddress("waveform1", wf1);
    tree->SetBranchAddress("waveform2", wf2);
    tree->SetBranchAddress("waveform3", wf3);
    tree->GetEvent(event);
    TGraph* gr0 = new TGraph(512, tt, wf0);
    TGraph* gr1 = new TGraph(512, tt, wf1);
    TGraph* gr2 = new TGraph(512, tt, wf2);
    TGraph* gr3 = new TGraph(512, tt, wf3);
    gr0->SetMinimum(150);
    gr0->SetMaximum(10000);
    gr0->Draw();
    c1->Update();
    gr1->Draw("same");
    gr2->Draw("same");
    gr3->Draw("same");
}
