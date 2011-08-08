/*
 *  SynapseOverride.cpp
 *  ncs5
 *
 *  Created by James King on 5/27/07.
 *  Copyright 2007 __MyCompanyName__. All rights reserved.
 *
 */

#include "SynapseOverride.h"
#include "Synapse.h"
#include "CellManager.h"
#include <iostream>
#include <fstream>
#include <string>
#include <sstream>

using namespace std;

SynapseOverride::SynapseOverride( T_EVENT *pEvent, CellManager *pCellManager, Brain *brain )
{
    //Find any cells on this node the Override targets
    int cellCount = 0;
    int *localCells = pCellManager->ListCellsOnNode( pEvent->cellGroup[0], pEvent->cellGroup[1], pEvent->cellGroup[2], &cellCount );
    
    if( cellCount <= 0 )
        return;
    
    ifstream fin( pEvent->file );
    if( !fin )  //should have already tested ability to open file, but double check
    {
        cout<<"Error: unable to open USE override file "<<pEvent->file<<endl;
        return;
    }
    
    //the file has two lines - the first has a map to compartment indexes (just as a sanity check)
    // the next line has the actual USE values
    string mapLine, valueLine;
    getline( fin, mapLine );
    getline( fin, valueLine );
    fin.close();
    
    //parse the values around white spaces
    vector<int> hostCellIDs;
    istringstream inID( mapLine );
    double cellID = 0;
    while( inID>>cellID )
        hostCellIDs.push_back( (int) cellID );
    istringstream inUSE( valueLine );
    double newUSE = 0;
    while( inUSE>>newUSE)
        replacementUSE.push_back( newUSE );
    
    int compartment = pEvent->cellGroup[3];
    for( int cellIndex=0, totalSyns=0; cellIndex<cellCount; cellIndex++ )
    {
        //check the compartment specified in the event for ownership of any synapses
        Compartment *cmpAccess = brain->Cells[ localCells[cellIndex]]->Compartments[compartment];
        
        for( int synapseIndex=0; synapseIndex<cmpAccess->nSynapse; synapseIndex++ )
        {
            if( pEvent->synapse == cmpAccess->SynapseList[synapseIndex]->SynDef->source->L.idx ) //detected a synapse match
            {
                synapseAccess.push_back( cmpAccess->SynapseList[synapseIndex] );
                
                //perform a sanity check that the hostCellIDs match what was in the file
                if( !(totalSyns < hostCellIDs.size()) || hostCellIDs[totalSyns++] != cellIndex )
                {
                     cout<<"Error in SynapseOverride.  Invalid synapse mapping\n";//out of bounds, or mismatch!
                     synapseAccess.clear();                     
                     return;
                }                
            }
        }
    }
        
    //validate that the synapse count matches the number of USE values given
    if( replacementUSE.size() != synapseAccess.size() )
    {
        cout<<"Error in SynapseOverride.  Mismatch in number of replacement USE values with number of synapse objects\n";
        synapseAccess.clear();
        return;
    }
        
    time = pEvent->time;
    
    free( localCells );
}

//----------------------------------------------------------------------------------

void SynapseOverride::execute() const
{
    //print current USE values, up through 10 synapses - before
    /*
    for( int synapseIndex=0; synapseIndex<synapseAccess.size() && synapseIndex < 10 ; synapseIndex++ )
        cout<< synapseAccess[synapseIndex]->USE<<" ";
    cout<<endl;
    */
    
    for( int synapseIndex=0; synapseIndex<synapseAccess.size(); synapseIndex++ )
        synapseAccess[synapseIndex]->USE = replacementUSE[synapseIndex];
    
    //and after    
    /*
    for( int synapseIndex=0; synapseIndex<synapseAccess.size() && synapseIndex < 10 ; synapseIndex++ )
        cout<< synapseAccess[synapseIndex]->USE<<" ";
    cout<<endl;
    */
}
